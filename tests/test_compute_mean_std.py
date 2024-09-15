import torch
from torch.utils.data import DataLoader, TensorDataset

from rgc.utils.data import compute_mean_std


def test_compute_mean_std():
    # Create a mock dataset with 3 channels
    data = torch.tensor([
        [[[1.0, 2.0], [3.0, 4.0]], [[2.0, 4.0], [6.0, 8.0]], [[0.5, 1.0], [1.5, 2.0]]],  # Batch 1, 3 channels
        [[[5.0, 6.0], [7.0, 8.0]], [[10.0, 12.0], [14.0, 16.0]], [[2.5, 3.0], [3.5, 4.0]]],  # Batch 2, 3 channels
        [[[9.0, 10.0], [11.0, 12.0]], [[18.0, 20.0], [22.0, 24.0]], [[4.5, 5.0], [5.5, 6.0]]],  # Batch 3, 3 channels
    ])

    targets = torch.tensor([0, 1, 2])  # Dummy target labels
    dataset = TensorDataset(data, targets)
    dataloader = DataLoader(dataset, batch_size=2)

    # Run the function
    mean, std = compute_mean_std(dataloader)

    # Expected mean and std for each channel based on the dataset
    expected_mean = torch.tensor([6.5000, 13.0000, 3.2500])  # Mean across all batches for each channel
    expected_std = torch.tensor([3.6056, 7.2111, 1.8028])  # Standard deviation across all batches for each channel

    # Check the mean and std are as expected
    assert torch.allclose(mean, expected_mean, atol=1e-4), f"Expected mean {expected_mean}, but got {mean}"
    assert torch.allclose(std, expected_std, atol=1e-4), f"Expected std {expected_std}, but got {std}"
