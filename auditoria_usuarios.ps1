$usuarios = Get-LocalUser
$sinLogon = @()
$conLogon = @()
foreach ($u in $usuarios){
    if (-not $u.LastLogon) {
        $sinLogon += "$($u.Name): Estado = $($u.Enabled), Último acceso = NUNCA"
    } else{
        $conLogon += "$($u.Name): Estado = $($u.Enabled), Último acceso = $($u.LastLogon)"
    }
}

Set-Content -Path "C:\Users\simon\Desktop\reporte_usuarios.txt" -Value "Usuarios que no han iniciado sesión"
ForEach ($usuario in $sinLogon) {
    Add-Content -Path "C:\Users\simon\Desktop\reporte_usuarios.txt" -Value $usuario
}
Add-Content -Path "C:\Users\simon\Desktop\reporte_usuarios.txt" -Value " "
Add-Content -Path "C:\Users\simon\Desktop\reporte_usuarios.txt" -Value "Usuarios que han iniciado sesión"
ForEach ($usuario in $conLogon) {
    Add-Content -Path "C:\Users\simon\Desktop\reporte_usuarios.txt" -Value $conLogon
}

if ($sinLogon -gt 0) {
    Write-Output "`n Usuarios que NUNCA han iniciado sesión"
    $sinLogon | ForEach-Object {Write-Output $_}
    if ($conLogon -gt 0) {
        Write-Output "`n Usuarios que SÍ han iniciado sesión"
        $conLogon | ForEach-Object {Write-Output $_}
    } else {
        Write-Output "Ningun usuario ha iniciado sesión"
    }
} else {
    Write-Output "Todos los usuarios han iniciado sesión"
    $conLogon | ForEach-Object {Write-Output $_}
}

