import os
import csv
import glob
import pandas as pd
from typing import Dict, List, Tuple, Optional, Iterator, Union, Set

class SVGDataLoader:
    """Utility for loading and managing SVG training data"""
    
    def __init__(self, base_dir: str = "/c:/Users/antoi/LLM2SVG/data"):
        """
        Initialize the data loader.
        
        Args:
            base_dir: Base directory containing the data
        """
        self.base_dir = base_dir
        self.train_dir = os.path.join(base_dir, "train")
        self.test_dir = os.path.join(base_dir, "test")
        self.train_csv = os.path.join(self.train_dir, "train.csv")
        self.test_csv = os.path.join(self.test_dir, "test.csv")
        
        # Cache for descriptions
        self._train_descriptions = None
        self._test_descriptions = None
    
    def get_train_descriptions(self) -> Dict[str, str]:
        """
        Get mapping of train sample IDs to descriptions.
        
        Returns:
            Dictionary mapping sample IDs to text descriptions
        """
        if self._train_descriptions is None:
            self._train_descriptions = self._load_descriptions(self.train_csv)
        return self._train_descriptions
    
    def get_test_descriptions(self) -> Dict[str, str]:
        """
        Get mapping of test sample IDs to descriptions.
        
        Returns:
            Dictionary mapping sample IDs to text descriptions
        """
        if self._test_descriptions is None:
            self._test_descriptions = self._load_descriptions(self.test_csv)
        return self._test_descriptions
    
    def _load_descriptions(self, csv_path: str) -> Dict[str, str]:
        """
        Load descriptions from a CSV file.
        
        Args:
            csv_path: Path to the CSV file
            
        Returns:
            Dictionary mapping sample IDs to text descriptions
        """
        descriptions = {}
        try:
            df = pd.read_csv(csv_path)
            for _, row in df.iterrows():
                descriptions[row['id']] = row['description']
        except Exception as e:
            print(f"Error loading descriptions from {csv_path}: {e}")
            # Fallback to standard CSV reader if pandas fails
            try:
                with open(csv_path, 'r', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        descriptions[row['id']] = row['description']
            except Exception as e2:
                print(f"CSV fallback failed: {e2}")
        
        return descriptions
    
    def get_svg_paths(self, split: str = "train") -> Dict[str, List[str]]:
        """
        Get paths to all SVG files in the dataset.
        
        Args:
            split: Dataset split ("train" or "test")
            
        Returns:
            Dictionary mapping sample IDs to lists of SVG file paths
        """
        base_dir = self.train_dir if split == "train" else self.test_dir
        svg_paths = {}
        
        # Search for all sample directories
        for sample_dir in os.listdir(os.path.join(base_dir, "svg")):
            sample_id = sample_dir
            sample_svg_dir = os.path.join(base_dir, "svg", sample_id, "svg")
            
            # If the directory exists, find all SVGs
            if os.path.exists(sample_svg_dir):
                svg_files = glob.glob(os.path.join(sample_svg_dir, "*.svg"))
                svg_paths[sample_id] = svg_files
            else:
                # For the structure shown in the tree, SVGs might be directly in the directory
                alt_svg_dir = os.path.join(base_dir, "svg", sample_id)
                if os.path.exists(alt_svg_dir):
                    svg_files = glob.glob(os.path.join(alt_svg_dir, "*.svg"))
                    if svg_files:
                        svg_paths[sample_id] = svg_files
        
        return svg_paths
    
    def load_all_svgs(self, split: str = "train") -> Dict[str, Dict[str, str]]:
        """
        Load all SVG files from the dataset.
        
        Args:
            split: Dataset split ("train" or "test")
            
        Returns:
            Dictionary mapping sample IDs to dictionaries of SVG file names to SVG content
        """
        svg_paths = self.get_svg_paths(split)
        svg_contents = {}
        
        for sample_id, paths in svg_paths.items():
            svg_contents[sample_id] = {}
            for path in paths:
                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        file_name = os.path.basename(path)
                        svg_contents[sample_id][file_name] = f.read()
                except Exception as e:
                    print(f"Error loading SVG {path}: {e}")
        
        return svg_contents
    
    def get_train_samples(self) -> List[Tuple[str, str, str]]:
        """
        Get list of training samples with descriptions and SVG paths.
        
        Returns:
            List of tuples (sample_id, description, svg_path)
        """
        descriptions = self.get_train_descriptions()
        svg_paths = self.get_svg_paths("train")
        
        samples = []
        for sample_id, paths in svg_paths.items():
            if sample_id in descriptions:
                for path in paths:
                    samples.append((sample_id, descriptions[sample_id], path))
            else:
                print(f"Warning: No description found for sample {sample_id}")
        
        return samples
    
    def get_test_samples(self) -> List[Tuple[str, str]]:
        """
        Get list of test samples with descriptions.
        
        Returns:
            List of tuples (sample_id, description)
        """
        descriptions = self.get_test_descriptions()
        return [(sample_id, description) for sample_id, description in descriptions.items()]
