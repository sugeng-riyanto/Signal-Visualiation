import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Oscilloscope wave generator function
def generate_wave(wave_type, freq, amp, phase, t):
    if wave_type == 'Sine':
        return amp * np.sin(2 * np.pi * freq * t + phase)
    elif wave_type == 'Square':
        return amp * np.sign(np.sin(2 * np.pi * freq * t + phase))
    elif wave_type == 'Triangle':
        return amp * (2 * np.arcsin(np.sin(2 * np.pi * freq * t + phase)) / np.pi)
    elif wave_type == 'Sawtooth':
        return amp * (2 * (t * freq - np.floor(0.5 + t * freq)))
    elif wave_type == 'Random':
        return amp * np.random.uniform(-1, 1, len(t))
    else:
        return np.zeros_like(t)

# FFT analysis function
def perform_fft(signal, sample_rate):
    N = len(signal)
    fft_result = np.fft.fft(signal)
    fft_freq = np.fft.fftfreq(N, d=1/sample_rate)
    magnitude = np.abs(fft_result)[:N // 2] * 2 / N  # Take only positive frequencies
    phase = np.angle(fft_result)[:N // 2]
    return fft_freq[:N // 2], magnitude, phase

# Function to plot waveform
def plot_waveform(t, wave, voltage_div, time_div, title):
    plt.figure(figsize=(10, 6))
    plt.plot(t, wave)
    plt.title(title)
    plt.xlabel(f'Time (s) [Time/Div: {time_div} s/div]')
    plt.ylabel(f'Voltage (V) [Voltage/Div: {voltage_div} V/div]')
    plt.grid(True)
    plt.ylim([-voltage_div * 10, voltage_div * 10])  # Adjust vertical scale
    plt.xlim([t[0], t[-1]])  # Adjust horizontal scale
    st.pyplot(plt)

# Function to plot FFT (Magnitude and Phase)
def plot_fft(fft_freq, magnitude, phase, log_scale=False):
    # Plot Magnitude Spectrum
    plt.figure(figsize=(10, 6))
    if log_scale:
        magnitude_db = 20 * np.log10(magnitude)  # Convert to dB
        plt.plot(fft_freq, magnitude_db)
        plt.title('Magnitude Spectrum (dB)')
        plt.ylabel('Magnitude (dB)')
    else:
        plt.plot(fft_freq, magnitude)
        plt.title('Magnitude Spectrum (Linear)')
        plt.ylabel('Magnitude')
    
    plt.xlabel('Frequency (Hz)')
    plt.grid(True)
    plt.xlim([0, np.max(fft_freq)])
    st.pyplot(plt)
    
    # Plot Phase Spectrum
    plt.figure(figsize=(10, 6))
    plt.plot(fft_freq, np.degrees(phase))
    plt.title('Phase Spectrum (Degrees)')
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Phase (Degrees)')
    plt.grid(True)
    plt.xlim([0, np.max(fft_freq)])
    st.pyplot(plt)

# Streamlit UI
st.title("Oscilloscope and FFT Simulation")

# Waveform settings
wave_type = st.selectbox('Select Wave Type', ['Sine', 'Square', 'Triangle', 'Sawtooth', 'Random', 'Superposition'])
freq = st.slider('Frequency (Hz)', min_value=20, max_value=20000, value=440)  # Audio sonic range
amp = st.slider('Amplitude (V)', min_value=0.1, max_value=5.0, value=1.0)
phase = st.slider('Phase (radians)', min_value=0.0, max_value=2 * np.pi, value=0.0)

# Voltage and Time divisions (oscilloscope settings)
voltage_div = st.slider('Voltage per Division (V/div)', min_value=0.1, max_value=10.0, value=1.0)
time_div = st.slider('Time per Division (s/div)', min_value=0.001, max_value=0.1, value=0.01)

# Time array based on selected time division
time_scale = 10  # Display 10 divisions on the oscilloscope
sample_rate = 1 / 0.0001  # Sample rate
t = np.arange(0, time_div * time_scale, 0.0001)  # Time vector with fine resolution

# Generate waveform
if wave_type == 'Superposition':
    # Superposition of two waves (Sine and Triangle for example)
    wave1 = generate_wave('Sine', freq, amp, phase, t)
    wave2 = generate_wave('Triangle', freq * 2, amp / 2, phase, t)
    wave = wave1 + wave2
    plot_waveform(t, wave, voltage_div, time_div, "Superposition of Sine and Triangle Waves")
else:
    wave = generate_wave(wave_type, freq, amp, phase, t)
    plot_waveform(t, wave, voltage_div, time_div, f'{wave_type} Wave')

# FFT Analysis
fft_freq, magnitude, phase = perform_fft(wave, sample_rate)

# Plot FFT (Magnitude and Phase) in both linear and dB scale
st.subheader("FFT Analysis")
st.write("Linear Scale")
plot_fft(fft_freq, magnitude, phase, log_scale=False)
st.write("Decibel (dB) Scale")
plot_fft(fft_freq, magnitude, phase, log_scale=True)
