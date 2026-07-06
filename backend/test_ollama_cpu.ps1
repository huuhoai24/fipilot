# Stop existing Ollama processes
Write-Output "Stopping existing Ollama processes..."
Stop-Process -Name ollama -Force -ErrorAction SilentlyContinue
Stop-Process -Name "ollama app" -Force -ErrorAction SilentlyContinue
Start-Sleep -Seconds 2

# Set environment variable to hide GPU
$env:CUDA_VISIBLE_DEVICES = ""
$env:OLLAMA_DEBUG = "1"

# Start ollama server in the background
Write-Output "Starting Ollama server in CPU-only mode..."
$serverProcess = Start-Process -FilePath "ollama" -ArgumentList "serve" -NoNewWindow -PassThru

# Wait for server to start up
Start-Sleep -Seconds 5

# Test run the model
Write-Output "Testing model run..."
ollama run gemma4:e2b "Xin chào, hãy giới thiệu ngắn gọn về bản thân."

# Wait a bit to capture output
Start-Sleep -Seconds 5
