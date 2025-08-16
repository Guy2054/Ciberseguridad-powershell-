function Validar-Archivo {
    param ([string]$Ruta)
    
    try {
        if (Test-Path $Ruta) {
            $contenido = Get-Content $Ruta -ErrorAction Stop
            return "Archivo encontrado y accecible: $Ruta"
        } else {
            throw "El archivo no existe"
        }
    }
    catch {
        return "Error: $_"
    }
    finally {
        Write-Host "Validación finalizada para: $Ruta" -ForegroundColor Cyan
    }
}

Validar-Archivo -Ruta "C:\archivo_inexistente"

Validar-Archivo -Ruta "$env:USERPROFILE\Desktop\archivo.txt"
