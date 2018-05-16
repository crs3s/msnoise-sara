from collections import OrderedDict
default = OrderedDict()

default['analysis_duration'] = ["Duration of the Analysis (total in seconds : 3600, [86400])",'86400']
default['preprocess_sampling_rate'] = ["Sampling Rate for the SARA PreProcessing [20.0]",'20.0']
default['resampling_method'] = ["Resampling method [Lanczos]/Decimate",'Lanczos']
default['decimation_factor'] = ["If Resampling mether=Decimate, decimation factor [5]",'5']
default['preprocess_lowpass'] = ["Preprocessing Low-pass value in Hz [9.0]",'9.0']
default['preprocess_highpass'] = ["Preprocessing High-pass value in Hz [5.0]",'5.0']
default['preprocess_taper_length'] = ["Length of the taper is seconds (5.0)]",'5.0']

default['components_to_compute'] = ["List (comma separated) [ZZ]", 'ZZ']

default['env_sampling_rate'] = ["Sampling Rate for the Envelopes [1.0]",'1.0']





