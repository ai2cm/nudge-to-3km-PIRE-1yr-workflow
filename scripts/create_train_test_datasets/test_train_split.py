import intake
import xarray as xr
import yaml
import numpy as np
import copy
import os
import vcm
from toolz import partition_all
from loaders.mappers import open_nudge_to_fine, open_zarr

# 60 train times drawn from 2 week block, from which first/last two timesteps are excluded
# 5 test times drawn from 1 week block following three week training block
# repeat x 13

STEPS_PER_WEEK = 56 # 3 hr sampling
TRAIN_BLOCK_SIZE= 2 * STEPS_PER_WEEK
TEST_BLOCK_SIZE = 1 * STEPS_PER_WEEK
PAD = 2  # exclude this number of samples from the ends of the train block



nudged_run_path = "gs://vcm-ml-experiments/n2f-pire-sfc-updates/2022-01-21/nudged-run/fv3gfs_run/"
rad_fluxes_path = "gs://vcm-ml-experiments/n2f-pire-sfc-updates/data/rad-train-test-data-time-centered-with-toa.zarr"

def split_times(times):
    train, test = [], []

    i = 0

    while i < len(times) :
        train_block = times[i + PAD: i + TRAIN_BLOCK_SIZE - PAD]
        test_block = times[i + TRAIN_BLOCK_SIZE: i + TRAIN_BLOCK_SIZE+ TEST_BLOCK_SIZE]
        
        train += train_block
        test += test_block
        i += TRAIN_BLOCK_SIZE+ TEST_BLOCK_SIZE
        
        
    np.random.seed(0)
    np.random.shuffle(train)
    np.random.shuffle(test) 
    return train, test   


def sort_within_batches(times, timesteps_per_batch):
    # Within batches of randomly sampled times, sort the timesteps for faster loading if shuffle_timesteps=false.
    # Samples within each batch of timesteps will be shuffled by tf dataset during training.
    batches = list(partition_all(timesteps_per_batch, times))
    sorted_batches = [sorted(batch) for batch in batches]
    flattened_sorted_batches = []
    for batch in sorted_batches:
        flattened_sorted_batches += batch
    return flattened_sorted_batches



def fill_timesteps(timesteps, template_path, output_path):
    with open(template_path, "r") as f:
        template_config = yaml.safe_load(f)
    config_ = copy.copy(template_config)
    config_["timesteps"] = timesteps
    with open(output_path, "w") as f:
        yaml.dump(config_, f, indent=4)    
    print(f"Filled timesteps saved in {output_path} using base configuration from {template_path}.")


mapper = open_nudge_to_fine(
    data_path=nudged_run_path,
    nudging_variables=[],
)
t_full_tq = sorted(list(mapper.keys()))
train_times_tq, test_times_tq = split_times(t_full_tq)

#t_full_rad = [vcm.encode_time(t) for t in ds_rad.time.values]


train_tq_template_config_path = "train_data_template_tq.yaml"
test_tq_template_config_path = "test_data_template_tq.yaml"


fill_timesteps(
    train_times_tq, "train_data_template_tq.yaml", "train_data_tq.yaml"
)
fill_timesteps(
    test_times_tq, "test_data_template_tq.yaml", "test_data_tq.yaml"
)