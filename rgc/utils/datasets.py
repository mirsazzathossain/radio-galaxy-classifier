"""
Datasets for the BENT, RGZ20k, and MiraBest datasets.

- BENT is a dataset of 150x150 pixel images of NAT and WAT radio galaxies.
- RGZ20k is a unlabeled dataset of 150x150 pixel images of radio galaxies.
- MiraBest is a dataset of 150x150 pixel images of FR-I and FR-II radio galaxies.
"""

__author__ = "Mir Sazzat Hossain"


import os
import pickle
import tarfile
from typing import ClassVar, Optional

import numpy as np
import torch
import torchvision
from PIL import Image
from torch.utils.data import Dataset
from torchvision.datasets.utils import check_integrity, download_url


class Bent(Dataset):
    """
    A PyTorch dataset for the BENT data.

    :param data: The data tensor.
    :type data: torch.Tensor

    :param target: The target tensor.
    :type target: torch.Tensor
    """

    base_folder = "batches"
    url = "https://drive.google.com/file/d/1s3u9HKXCJmX_1DKv5Hp9fJS_b5DyfNHV"
    filename = "bent_batches.tar.gz"
    tgz_md5 = "b0f93db1d28dad0561da6f16243b1766"
    train_list: ClassVar[list] = [
        ["data_batch_0", "50d49ca1d3da4adab4a9995789524297"],
        ["data_batch_1", "c5b99ce3457651013f48bbf894ed03f5"],
        ["data_batch_2", "8fb2c8c90d295babb317ca8df93e6bbe"],
        ["data_batch_3", "858178ae4b2facd6234efa1d7eb5cd42"],
        ["data_batch_4", "c6431b63801c69959dbd66a2e0c0e806"],
        ["data_batch_5", "8ae7d9b4492b1e52f766dbeed0d3a02c"],
        ["data_batch_6", "43a5cf61c3a8b314d3dece7043e94d56"],
        ["data_batch_7", "8a45db626670e50e2aebd75b0bf35b4a"],
        ["data_batch_8", "4511c9175d861e75e00e0bea968c586a"],
    ]

    test_list: ClassVar[list] = [["test_batch", "559a2d8336d673f1025a8682a91a4914"]]

    meta: ClassVar[dict] = {
        "filename": "batches.meta",
        "key": "labels",
        "md5": "214499a9b09597e8cbb6cd951debe1cc",
    }

    def __init__(
        self,
        root: str,
        train: bool = True,
        transform: Optional[torchvision.transforms.Compose] = None,
        target_transform: Optional[torchvision.transforms.Compose] = None,
        download: bool = False,
        include_small: bool = False,
    ) -> None:
        """
        Initialize the BENT dataset.

        :param root: The root directory of the dataset.
        :type root: str
        :param train: If True, creates a dataset from the training set, otherwise from the test set.
        :type train: bool
        :param transform: A function/transform that takes in an PIL image and returns a transformed version.
        :type transform: Optional[torchvision.transforms.Compose]
        :param target_transform: A function/transform that takes in the target and transforms it.
        :type target_transform: Optional[torchvision.transforms.Compose]
        :param download: If True, downloads the dataset from the internet and puts it in root directory.
        :type download: bool
        :param include_small: If True, includes the small dataset.
        :type include_small: bool
        """
        self.root = os.path.expanduser(root)
        self.transform = transform
        self.target_transform = target_transform
        self.train = train
        self.include_small = include_small

        if download:
            self.download()

        if not self._check_integrity():
            raise RuntimeError("Dataset not found or corrupted. You can use download=True to download it.")  # noqa: TRY003

        downloaded_list = self.train_list if self.train else self.test_list
        self.data = []
        self.target = []

        for file_name, _ in downloaded_list:
            file_path = os.path.join(self.root, self.base_folder, file_name)

            with open(file_path, "rb") as infile:
                entry = pickle.load(infile, encoding="latin1")  # noqa: S301

            labels = entry["labels"] if "labels" in entry else entry["fine_labels"]

            for i, label in enumerate(labels):
                if not self.include_small:
                    if label not in ["101", "201"]:
                        self.data.append(entry["data"][i])
                        label = 0 if label == "100" else 1
                        self.target.append(label)
                    else:
                        continue
                else:
                    print("Including small dataset." + label)
                    self.data.append(entry["data"][i])
                    label = 0 if label in ["100", "101"] else 1
                    self.target.append(label)

        self.data = np.array(self.data).reshape(-1, 1, 150, 150)
        self.data = self.data.transpose((0, 2, 3, 1))

        self._load_meta()

    def _load_meta(self) -> None:
        """
        Load the metadata of the dataset.
        """
        path = os.path.join(self.root, self.base_folder, self.meta["filename"])
        if not check_integrity(path, self.meta["md5"]):
            raise RuntimeError("Dataset metadata not found or corrupted. You can use download=True to download it.")  # noqa: TRY003

        with open(path, "rb") as infile:
            data = pickle.load(infile, encoding="latin1")  # noqa: S301
            self.classes = data[self.meta["key"]]
        self.class_to_idx = {_class: i for i, _class in enumerate(self.classes)}

    def __getitem__(self, index: int) -> tuple[torch.Tensor, torch.Tensor]:
        """
        Get an item from the dataset.

        :param index: The index of the item.
        :type index: int

        :return: The data and target tensors.
        :rtype: tuple[torch.Tensor, torch.Tensor]
        """
        img, target = self.data[index], self.target[index]

        img = np.reshape(img, (150, 150))
        img = Image.fromarray(img, mode="L")

        if self.transform is not None:
            img = self.transform(img)

        if self.target_transform is not None:
            target = self.target_transform(target)

        return img, target

    def __len__(self) -> int:
        """
        Get the length of the dataset.

        :return: The length of the dataset.
        :rtype: int
        """
        return len(self.data)

    def _check_integrity(self) -> bool:
        """
        Check the integrity of the dataset.

        :return: True if the dataset is found and intact, False otherwise.
        :rtype: bool
        """
        root = self.root
        for fentry in self.train_list + self.test_list:
            filename, md5 = fentry
            fpath = os.path.join(root, self.base_folder, filename)
            if not check_integrity(fpath, md5):
                return False
        return True

    def download(self) -> None:
        """
        Download the BENT dataset.
        """
        if self._check_integrity():
            print("Files already downloaded and verified")
            return

        download_url(self.url, self.root, self.filename, self.tgz_md5)

        with tarfile.open(os.path.join(self.root, self.filename), "r:gz") as tar:
            tar.extractall(path=self.root)  # noqa: S202

    def __repr__(self) -> str:
        """
        Get the representation of the dataset.

        :return: The representation of the dataset.
        :rtype: str
        """
        fmt_str = "Dataset " + self.__class__.__name__ + "\n"
        fmt_str += f"    Number of datapoints: {self.__len__()}\n"
        tmp = "train" if self.train is True else "test"
        fmt_str += f"    Split: {tmp}\n"
        fmt_str += f"    Root Location: {self.root}\n"
        tmp = "    Transforms (if any): {}\n".format(self.transform.__repr__().replace("\n", "\n" + " " * 29))
        fmt_str += tmp
        tmp = "    Target Transforms (if any): {}\n".format(
            self.target_transform.__repr__().replace("\n", "\n" + " " * 29)
        )
        fmt_str += tmp
        return fmt_str


class RGZ20k(Dataset):
    """`RGZ 20K`_Dataset from https://github.com/inigoval/byol

    Args:
        root (string): Root directory of dataset where directory
            ``htru1-batches-py`` exists or will be saved to if download is set to True.
        train (bool, optional): If True, creates dataset from training set, otherwise
            creates from test set.
        transform (callable, optional): A function/transform that takes in an PIL image
            and returns a transformed version. E.g, ``transforms.RandomCrop``
        target_transform (callable, optional): A function/transform that takes in the
            target and transforms it.
        download (bool, optional): If true, downloads the dataset from the internet and
            puts it in root directory. If dataset is already downloaded, it is not
            downloaded again.

    """

    base_folder = "rgz20k-batches-py"
    url = "http://www.jb.man.ac.uk/research/ascaife/rgz20k-batches-python.tar.gz"
    filename = "rgz20k-batches-python.tar.gz"
    tgz_md5 = "3a85fb4167fb08619e36e77bbba40896"
    train_list: ClassVar[list] = [
        ["data_batch_1", "9ffdcb485fc0c96e1afa1cdc342f00e7"],
        ["data_batch_2", "8961fa4a2fb5a8482ec5606e3d501fb4"],
        ["data_batch_3", "8cbf4fa7b34282b8f1522a350df4a882"],
        ["data_batch_4", "a58c94b5905d0ad2d97ba3a8895538c9"],
        ["data_batch_5", "13c9132ee374b7b63dac22c17a412d86"],
        ["data_batch_6", "232ff5854df09d5a68471861b1ee5576"],
        ["data_batch_7", "bea739fe0f7bd6ffb77b8e7def7f2edf"],
        ["data_batch_8", "48b23b3f0f37478b61ccca462fe53917"],
        ["data_batch_9", "2ac1208dec744cc136d0cd7842c180a2"],
        ["data_batch_10", "4ad68d1d8179da93ca1f8dfa7fe8e11d"],
    ]

    test_list: ClassVar[list] = [["test_batch", "35a588227816ad08d37112f23b6e2ea4"]]
    meta: ClassVar[dict] = {
        "filename": "batches.meta",
        "key": "label_names",
        "md5": "8f3138fbc912134239a779a1f3f6eaf8",
    }

    def __init__(
        self,
        root,
        train=True,
        transform=None,
        target_transform=None,
        download=False,
        remove_duplicates: bool = True,
        cut_threshold: float = 0.0,
        mb_cut=False,
    ):
        self.root = os.path.expanduser(root)
        self.transform = transform
        self.target_transform = target_transform
        self.train = train  # training set or test set
        self.remove_duplicates = remove_duplicates
        self.cut_threshold = cut_threshold
        self.mb_cut = mb_cut

        if download:
            self.download()

        if not self._check_integrity():
            raise RuntimeError("Dataset not found or corrupted." + " You can use download=True to download it")

        downloaded_list = self.train_list if self.train else self.test_list

        self.data = []  # object image data
        self.names = []  # object file names
        self.rgzid = []  # object RGZ ID
        self.mbflg = []  # object MiraBest flag
        self.sizes = []  # object largest angular sizes

        # now load the picked numpy arrays
        for file_name, _ in downloaded_list:
            file_path = os.path.join(self.root, self.base_folder, file_name)

            with open(file_path, "rb") as f:
                entry = pickle.load(f, encoding="latin1")  # noqa: S301

                self.data.append(entry["data"])
                self.names.append(entry["filenames"])
                self.rgzid.append(entry["src_ids"])
                self.mbflg.append(entry["mb_flag"])
                self.sizes.append(entry["LAS"])

        self.rgzid = np.vstack(self.rgzid).reshape(-1)
        self.sizes = np.vstack(self.sizes).reshape(-1)
        self.mbflg = np.vstack(self.mbflg).reshape(-1)
        self.names = np.vstack(self.names).reshape(-1)

        self.data = np.vstack(self.data).reshape(-1, 1, 150, 150)
        self.data = self.data.transpose((0, 2, 3, 1))

        self._load_meta()

        # Make cuts on the data
        n = self.__len__()
        idx_bool = np.ones(n, dtype=bool)

        if self.remove_duplicates:
            print(f"Removing duplicates from RGZ dataset...")  # noqa: F541
            idx_bool = np.zeros(n, dtype=bool)
            _, idx_unique = np.unique(self.data, axis=0, return_index=True)
            idx_bool[idx_unique] = True

            print(f"Removed {n - np.count_nonzero(idx_bool)} duplicate samples")
            n = np.count_nonzero(idx_bool)

        idx_bool *= self.sizes > self.cut_threshold
        print(f"Removing {n - np.count_nonzero(idx_bool)} samples below angular size threshold.")
        n = np.count_nonzero(idx_bool)

        if mb_cut:
            idx_bool *= self.mbflg == 0

            # Print number of MB samples removed
            print(f"Removed {n - np.count_nonzero(idx_bool)} MiraBest samples from RGZ")

        idx = np.argwhere(idx_bool).squeeze()

        self.data = self.data[idx]
        self.names = self.names[idx]
        self.rgzid = self.rgzid[idx]
        self.mbflg = self.mbflg[idx]
        self.sizes = self.sizes[idx]

    def _load_meta(self):
        path = os.path.join(self.root, self.base_folder, self.meta["filename"])
        if not check_integrity(path, self.meta["md5"]):
            raise RuntimeError(
                "Dataset metadata file not found or corrupted." + " You can use download=True to download it"
            )
        with open(path, "rb") as infile:
            data = pickle.load(infile, encoding="latin1")  # noqa: S301

            self.classes = data[self.meta["key"]]

    def __getitem__(self, index):
        """
        Args:
            index (int): Index

        Returns:
            image (array): Image
        """

        img = self.data[index]
        las = self.sizes[index].squeeze()
        mbf = self.mbflg[index].squeeze()
        rgz = self.rgzid[index].squeeze()

        img = img.squeeze()
        img = Image.fromarray(img, mode="L")

        if self.transform is not None:
            img = self.transform(img)

        return img, {"size": las, "mb": mbf, "id": rgz, "index": index}

    def __len__(self):
        return len(self.data)

    def _check_integrity(self):
        root = self.root
        for fentry in self.train_list + self.test_list:
            filename, md5 = fentry[0], fentry[1]
            fpath = os.path.join(root, self.base_folder, filename)
            if not check_integrity(fpath, md5):
                return False
        return True

    def download(self):
        import tarfile

        if self._check_integrity():
            print("Files already downloaded and verified")
            return

        download_url(self.url, self.root, self.filename, self.tgz_md5)

        with tarfile.open(os.path.join(self.root, self.filename), "r:gz") as tar:
            tar.extractall(path=self.root)  # noqa: S202

    def __repr__(self):
        fmt_str = "Dataset " + self.__class__.__name__ + "\n"
        fmt_str += f"    Number of datapoints: {self.__len__()}\n"
        tmp = "train" if self.train is True else "test"
        fmt_str += f"    Split: {tmp}\n"
        fmt_str += f"    Root Location: {self.root}\n"
        tmp = "    Transforms (if any): "
        fmt_str += "{}{}\n".format(tmp, self.transform.__repr__().replace("\n", "\n" + " " * len(tmp)))
        tmp = "    Target Transforms (if any): "
        fmt_str += "{}{}".format(tmp, self.target_transform.__repr__().replace("\n", "\n" + " " * len(tmp)))
        return fmt_str

    def get_from_id(self, rgz_id):
        index = np.argwhere(self.rgzid.squeeze() == rgz_id).squeeze()

        img = self.data[index]
        img = np.reshape(img, (150, 150))
        img = Image.fromarray(img, mode="L")

        if self.transform is not None:
            img = self.transform(img)

        return img


class MiraBest(Dataset):
    """MiraBest Dataset from https://zenodo.org/records/4288837

    Args:
        root (string): Root directory of dataset where directory
            ``MiraBest.py` exists or will be saved to if download is set to True.
        train (bool, optional): If True, creates dataset from training set, otherwise
            creates from test set.
        transform (callable, optional): A function/transform that takes in an PIL image
            and returns a transformed version. E.g, ``transforms.RandomCrop``
        target_transform (callable, optional): A function/transform that takes in the
            target and transforms it.
        download (bool, optional): If true, downloads the dataset from the internet and
            puts it in root directory. If dataset is already downloaded, it is not
            downloaded again.

    """

    base_folder = "batches"
    url = "http://www.jb.man.ac.uk/research/MiraBest/basic/MiraBest_basic_batches.tar.gz"
    filename = "MiraBest_basic_batches.tar.gz"
    tgz_md5 = "6c9a3e6ca3c0f3d27f9f6dca1b9730e1"
    train_list: ClassVar[list] = [
        ["data_batch_1", "6c501a41da89217c7fda745b80c06e99"],
        ["data_batch_2", "e4a1e5d6f1a17c65a23b9a80969d70fb"],
        ["data_batch_3", "e326df6fe352b669da8bf394e8ac1644"],
        ["data_batch_4", "7b9691912178497ad532c575e0132d1f"],
        ["data_batch_5", "de822b3c21f13c188d5fa0a08f9fcce2"],
        ["data_batch_6", "39b38c3d63e595636509f5193a98d6eb"],
        ["data_batch_7", "f980bfd2b1b649f6142138f2ae76d087"],
        ["data_batch_8", "a5459294e551984ac26056ba9f69a3f8"],
        ["data_batch_9", "34414bcae9a2431b42a7e1442cb5c73d"],
    ]

    test_list: ClassVar[list] = [
        ["test_batch", "d12d31f7e8d60a8d52419a57374d0095"],
    ]
    meta: ClassVar[dict] = {
        "filename": "batches.meta",
        "key": "label_names",
        "md5": "97de0434158b529b5701bb3a1ed28ec6",
    }

    def __init__(self, root, train=True, transform=None, target_transform=None, download=False):
        self.root = os.path.expanduser(root)
        self.transform = transform
        self.target_transform = target_transform
        self.train = train  # training set or test set

        if download:
            self.download()

        if not self._check_integrity():
            raise RuntimeError("Dataset not found or corrupted." + " You can use download=True to download it")

        downloaded_list = self.train_list if self.train else self.test_list

        self.data = []
        self.targets = []

        # now load the picked numpy arrays
        for file_name, _ in downloaded_list:
            file_path = os.path.join(self.root, self.base_folder, file_name)

            with open(file_path, "rb") as f:
                entry = pickle.load(f, encoding="latin1")  # noqa: S301

                self.data.append(entry["data"])
                if "labels" in entry:
                    self.targets.extend(entry["labels"])
                else:
                    self.targets.extend(entry["fine_labels"])

        self.data = np.vstack(self.data).reshape(-1, 1, 150, 150)
        self.data = self.data.transpose((0, 2, 3, 1))

        self._load_meta()

    def _load_meta(self):
        path = os.path.join(self.root, self.base_folder, self.meta["filename"])
        if not check_integrity(path, self.meta["md5"]):
            raise RuntimeError(
                "Dataset metadata file not found or corrupted." + " You can use download=True to download it"
            )
        with open(path, "rb") as infile:
            data = pickle.load(infile, encoding="latin1")  # noqa: S301
            self.classes = data[self.meta["key"]]
        self.class_to_idx = {_class: i for i, _class in enumerate(self.classes)}

    def __getitem__(self, index):
        """
        Args:
            index (int): Index

        Returns:
            tuple: (image, target) where target is index of the target class.
        """
        img, target = self.data[index], self.targets[index]

        # doing this so that it is consistent with all other datasets
        # to return a PIL Image
        img = np.reshape(img, (150, 150))
        img = Image.fromarray(img, mode="L")

        if self.transform is not None:
            img = self.transform(img)

        if self.target_transform is not None:
            target = self.target_transform(target)

        return img, target

    def __len__(self):
        return len(self.data)

    def _check_integrity(self):
        root = self.root
        for fentry in self.train_list + self.test_list:
            filename, md5 = fentry[0], fentry[1]
            fpath = os.path.join(root, self.base_folder, filename)
            if not check_integrity(fpath, md5):
                return False
        return True

    def download(self):
        import tarfile

        if self._check_integrity():
            print("Files already downloaded and verified")
            return

        download_url(self.url, self.root, self.filename, self.tgz_md5)

        # extract file
        with tarfile.open(os.path.join(self.root, self.filename), "r:gz") as tar:
            tar.extractall(path=self.root)  # noqa: S202

    def __repr__(self):
        fmt_str = "Dataset " + self.__class__.__name__ + "\n"
        fmt_str += f"    Number of datapoints: {self.__len__()}\n"
        tmp = "train" if self.train is True else "test"
        fmt_str += f"    Split: {tmp}\n"
        fmt_str += f"    Root Location: {self.root}\n"
        tmp = "    Transforms (if any): "
        fmt_str += "{}{}\n".format(tmp, self.transform.__repr__().replace("\n", "\n" + " " * len(tmp)))
        tmp = "    Target Transforms (if any): "
        fmt_str += "{}{}".format(tmp, self.target_transform.__repr__().replace("\n", "\n" + " " * len(tmp)))
        return fmt_str
