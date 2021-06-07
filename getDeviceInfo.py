import pyaudio

p = pyaudio.PyAudio()
devIndex = 11

devinfo = p.get_device_info_by_index(devIndex)  # Or whatever device you care about.
print(devinfo)
if p.is_format_supported(48000.0,  # Sample rate
                         input_device=devinfo['index'],
                         input_channels=devinfo['maxInputChannels'],
                         input_format=pyaudio.paInt16):
  print('Yay!')
