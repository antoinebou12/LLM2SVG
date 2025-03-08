import os
import torch
from typing import Dict, List, Tuple, Optional, Union, Callable
from torch.utils.data import Dataset, DataLoader

from utils.data_loader import SVGDataLoader
from utils.svg_constraints import SVGConstraints

class SVGDataset(Dataset):
    """Dataset for training SVG generation models"""
    
    def __init__(self, 
                 split: str = "train",
                 transform: Optional[Callable] = None,
                 data_dir: str = "/c:/Users/antoi/LLM2SVG/data",
                 validate_svgs: bool = True):
        """
        Initialize the SVG dataset.
        
        Args:
            split: Dataset split ("train" or "test")
            transform: Optional transform to apply to the data
            data_dir: Base directory containing the data
            validate_svgs: Whether to validate SVGs against constraints
        """
        self.split = split
        self.transform = transform
        self.loader = SVGDataLoader(data_dir)
        self.validate_svgs = validate_svgs
        
        if validate_svgs:
            self.svg_validator = SVGConstraints()
        
        # Load the data
        if split == "train":
            self.samples = self.loader.get_train_samples()
        else:
            # For test, we don't have SVG paths
            self.descriptions = self.loader.get_test_descriptions()
            self.samples = [(id, desc) for id, desc in self.descriptions.items()]
    
    def __len__(self) -> int:
        """Get the number of samples in the dataset."""
        return len(self.samples)
    
    def __getitem__(self, idx: int) -> Dict:
        """
        Get a sample from the dataset.
        
        Args:
            idx: Index of the sample
            
        Returns:
            Dictionary containing sample data
        """
        if self.split == "train":
            sample_id, description, svg_path = self.samples[idx]
            
            try:
                with open(svg_path, 'r', encoding='utf-8') as f:
                    svg_content = f.read()
                
                if self.validate_svgs:
                    try:
                        self.svg_validator.validate_svg(svg_content)
                    except ValueError as e:
                        print(f"Invalid SVG in {svg_path}: {e}")
                        svg_content = "<svg></svg>"  # Use empty SVG as fallback
                
                sample = {
                    'id': sample_id,
                    'description': description,
                    'svg_path': svg_path,
                    'svg_content': svg_content,
                }
                
                if self.transform:
                    sample = self.transform(sample)
                
                return sample
            except Exception as e:
                print(f"Error loading sample {sample_id} from {svg_path}: {e}")
                return {'id': sample_id, 'description': description, 'svg_content': "<svg></svg>"}
        else:
            # For test set, we just return the ID and description
            sample_id, description = self.samples[idx]
            return {'id': sample_id, 'description': description}

def create_data_loaders(batch_size: int = 32, num_workers: int = 4) -> Tuple[DataLoader, DataLoader]:
    """
    Create data loaders for training and testing.
    
    Args:
        batch_size: Batch size for data loading
        num_workers: Number of worker processes for data loading
        
    Returns:
        Tuple of (train_loader, test_loader)
    """
    train_dataset = SVGDataset(split="train")
    test_dataset = SVGDataset(split="test")
    
    train_loader = DataLoader(
        train_dataset,
        batch_size=batch_size,
        shuffle=True,
        num_workers=num_workers,
        collate_fn=collate_svg_batch,
    )
    
    test_loader = DataLoader(
        test_dataset,
        batch_size=batch_size,
        shuffle=False,
        num_workers=num_workers,
        collate_fn=collate_svg_batch,
    )
    
    return train_loader, test_loader

def collate_svg_batch(batch: List[Dict]) -> Dict[str, List]:
    """
    Collate function for batching SVG samples.
    
    Args:
        batch: List of sample dictionaries
        
    Returns:
        Dictionary of batched data
    """
    ids = [item['id'] for item in batch]
    descriptions = [item['description'] for item in batch]
    
    result = {
        'ids': ids,
        'descriptions': descriptions,
    }
    
    # Add SVG content if available
    if 'svg_content' in batch[0]:
        svg_contents = [item['svg_content'] for item in batch]
        result['svg_contents'] = svg_contents
    
    # Add SVG paths if available
    if 'svg_path' in batch[0]:
        svg_paths = [item['svg_path'] for item in batch]
        result['svg_paths'] = svg_paths
    
    return result
