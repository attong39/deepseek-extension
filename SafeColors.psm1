# Safe Write-Host function for all scripts
function Safe-WriteHost {
    param(
        [Parameter(Mandatory)] [string] $Message,
        [string] $Color = 'White'
    )
    $validColors = @('Black','DarkBlue','DarkGreen','DarkCyan','DarkRed','DarkMagenta','DarkYellow','Gray','DarkGray','Blue','Green','Cyan','Red','Magenta','Yellow','White')
    if ($validColors -notcontains $Color) { 
        $Color = 'Yellow' 
    }
    Write-Host $Message -ForegroundColor $Color
}

# Export function for use in other scripts
Export-ModuleMember -Function Safe-WriteHost
