import os
import whisper

def main():
    audio_folder = "MP3 audio"
    if not os.path.isdir(audio_folder):
        print(f"No folder named '{audio_folder}' found. Exiting.")
        return

    out_folder = os.path.join("Transcribed", "Audio")
    os.makedirs(out_folder, exist_ok=True)

    # Loads a Whisper model. 
    model = whisper.load_model("base")  # or "small", "medium", "large"...

    # Walks through MP3 files in "MP3 audio"
    for file_name in os.listdir(audio_folder):
        if file_name.lower().endswith(".mp3"):
            in_path = os.path.join(audio_folder, file_name)
            base_name = os.path.splitext(file_name)[0]
            out_txt = os.path.join(out_folder, base_name + ".txt")

            print(f"Transcribing: {file_name} ...")
            try:
                # Transcribes the data with Whisper
                result = model.transcribe(in_path)
                text = result["text"]

                # Writes resutls to text to file
                with open(out_txt, "w", encoding="utf-8") as f:
                    f.write(text)

            except Exception as e:
                print(f"Error transcribing {file_name}: {e}")

    print("\nAll done! Check 'Transcribed/lectures' for the .txt files.")

if __name__ == "__main__":
    main()
