import sys

# function to handle keyboard interrupt
def signal_handler(sig, frame):
    # delete the temporary file
	# tempVideo.cleanup()
	print("[INFO] You pressed `ctrl + c`! Closing mail detector" \
		" application...")
	sys.exit(0)

def fibo(n):
    return n * 4