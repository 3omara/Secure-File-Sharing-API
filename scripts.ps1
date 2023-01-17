switch ($args[0]) {
    "build_front" {
        .venv_win\Scripts\activate.ps1
        Set-Location frontend
        pyinstaller.exe --onefile --windowed --add-data "assets/app.ico;assets" --icon=assets/app.ico main.py
        Set-Location ..
    }
    "install_requirements" {
        .venv_win\Scripts\activate.ps1
        pip install -r requirements.txt
    }
    Default {
        Write-Output "Unknown command ($($args[0]))"
        Write-Output "Available commands: build_front"
    }
}