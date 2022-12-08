import uhd
import time
import numpy as np
import matplotlib.pyplot as plt
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("UHD driver test")


def receive_samples(
    usrp, center_frequency=900e6, sampling_rate=1e6, gain=50,
    recv_for=60, write_to_file=False, filename=None
):
    if write_to_file and filename is None:
        raise RuntimeError("Can't set write_to_file True without specifying a filename")
    logger.info("Receiving...")
    samples = []
    start = time.time()
    while time.time() - start < recv_for:
        samples.extend(
            usrp.recv_num_samps(1000, center_frequency, sampling_rate, [0], gain)[0]
        )
    logger.info(f"Received {len(samples)} samples")

    # Plot received sample in the Frequency Domain
    plt.psd(samples, NFFT=1024, Fs=1e6)
    plt.title("Frequency Domain")
    plt.show()

    # Plot received sample in the Time domain
    plt.plot(samples)
    plt.title("Time Domain")
    plt.show()

# Transmit example
def transmit_example(usrp):
    # Create a waveform
    # samples =  0.1 * np.random.randn(1000) + 0.1j * np.random.randn(1000)
    samples = np.sin(2*np.pi*100e3*np.arange(1000)/100e6)
    duration = 100  # seconds
    center_freq = 915e6
    sample_rate = 1e6
    gain = 50  # dB
    logger.info("Transmitting...")
    usrp.send_waveform(samples, duration, center_freq, sample_rate, [0], gain)
    logger.info("Done transmitting")


if __name__ == '__main__':
    # The USRP object
    usrp = uhd.usrp.MultiUSRP()
    usrp.set_rx_antenna("TX/RX", 0)

    receive_samples(usrp)
    # transmit_example(usrp)
