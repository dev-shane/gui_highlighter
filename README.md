# GUI Highlighter

This tool parses Android UI XML files and highlights **leaf-level GUI components** in corresponding screenshots. The output is a set of annotated images where interactive components are outlined for easier visualization.

---

## 1. Clone the repository

```bash
git clone <repository-url>
cd gui_highlighter
````

> Make sure you `cd` into the repository folder before continuing. All paths in the instructions assume you are in the root of the cloned repository.

---

## 2. Python Version Requirement

This project requires Python 3.10 or higher. You can check your Python version with:

```powershell
python --version
```
or

```bash
python3 --version
```

---

## 3. Create and activate a virtual environment (venv)

### Windows (PowerShell)

```powershell
python -m venv venv
.\venv\Scripts\activate
```

### Mac / Linux (bash)

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 4. Install dependencies

The project only requires **Pillow** for image processing:

```bash
pip install pillow
```
> Run in the terminal to install required libraries.

---

## 5. Project structure and data placement

Your project should have the following structure:

```
gui_highlighter/
│
├─ src/
│   ├─ main.py
│   ├─ parser.py
│   └─ drawer.py
│
├─ data/
│   ├─ <app.package>-<screen#>.xml
│   └─ <app.package>-<screen#>.png
│
└─ output/  (this will be created automatically)
```

* Place all screenshot/XML pairs in the `data/` folder.
* Each XML file must have a corresponding PNG file with the same name (only the extension differs).

---

## 6. Run the program

### Basic run

```bash
python -m src.main
```

⚠️ Make sure you are in the root of the repository when running this command, otherwise relative paths to `data/` and `output/` will not work.

### Specify a custom output folder

```bash
python -m src.main --output-dir annotated_images
```

Annotated images will be saved to the specified folder.

---

## 7. Notes

* Ensure that each XML has a corresponding PNG. Missing files will be skipped.
* The program logs processing details to `app.log`. 
* Any errors will also be printed in the console.
* You do not need to compile the code—Python scripts run directly in the virtual environment.