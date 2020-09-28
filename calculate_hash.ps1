foreach ($file in (Get-Content .\hash_path.txt))
    {
        Get-FileHash $file -Algorithm sha256 | Select-Object -Property path,hash
       
    }