import shutil
import subprocess


def main() -> None:
	adt_path = shutil.which("adt")
	assert adt_path is not None
	certificate_output_path = "./output.crt"
	signing_certificate_making_command = [
		adt_path, "-certificate",
		"-cn",  "RequiemWorld",
		"-validityPeriod", "15",  # years
		"2048-RSA",  # key
		certificate_output_path,  # output
		"password"]
	subprocess.check_output(signing_certificate_making_command)


if __name__ == '__main__':
	main()