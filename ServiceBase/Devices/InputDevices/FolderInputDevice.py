import os

from Devices.InputDevices.BaseInputDevice import BaseInputDevice


class FolderInputDevice(BaseInputDevice):
    def __init__(self, serializer, device_name, path):
        BaseInputDevice.__init__(self, serializer, device_name)
        self.path = path
        self.device_name = device_name
        self.current_file = None
        os.makedirs(os.path.join(self.path, "inProgress"), exist_ok=True)
        os.makedirs(os.path.join(self.path, "Done"), exist_ok=True) # for debugging purposes only
        # todo - mvoe inprogress content back to queue

    def _get_oldest_file_name(self):
        list_of_files = os.listdir(self.path)
        list_of_files = [path for path in list_of_files if not os.path.isdir(os.path.join(self.path, path))]
        if list_of_files:
            full_paths = ["{0}/{1}".format(self.path, x) for x in list_of_files]
            oldest_file = min(full_paths, key=os.path.getctime)
            return oldest_file
        return None

    def __enter__(self):
        oldest_file_path = self._get_oldest_file_name()
        if oldest_file_path:
            in_progress_path = os.path.join(self.path, "inProgress", os.path.basename(oldest_file_path))
            os.rename(oldest_file_path, in_progress_path)
            self.current_file = open(in_progress_path, "r",encoding='utf-8-sig')

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.current_file:
            file_name = self.current_file.name
            in_progress_path = os.path.join(self.path, "inProgress", os.path.basename(file_name))
            done_path = os.path.join(self.path, "Done", os.path.basename(file_name))  # for debugging purposes only
            backout_path = os.path.join(self.path, os.path.basename(file_name))
            self.current_file.close()
            self.current_file = None
            if not exc_type:
                os.rename(in_progress_path, done_path)   # for debugging purposes only-todo should delete msg from queue
                # os.remove(in_progress_path)
            else:
                os.rename(in_progress_path, backout_path)

    def get_products(self):
        if self.current_file:
            metadata = {"filename": os.path.basename(self.current_file.name),
                        "directory": os.path.dirname(self.current_file.name)}

            stream = self.current_file.read()
            product = self.serializer.deserialize(stream, **metadata)

            yield product
