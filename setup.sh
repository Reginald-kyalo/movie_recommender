mkdir -p ~/.streamlit/

echo "\
[server] 
port = ${PORT:-8501} 
enableCORS = false 
headless = true 
" > ~/.streamlit/config.toml