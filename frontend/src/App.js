import React, { useState } from 'react'; // Import useState
import logo from './logo.svg';
import './App.css';

function App() {
  // State for the command input
  const [command, setCommand] = useState('');
  // State for the API response
  const [result, setResult] = useState(null);
  // State for loading status
  const [isLoading, setIsLoading] = useState(false);
  // State for error messages
  const [error, setError] = useState(null);

  const handleInputChange = (event) => {
    setCommand(event.target.value);
  };

  const handleSubmit = async (event) => {
    event.preventDefault(); // Prevent default form submission
    setIsLoading(true);
    setError(null);
    setResult(null);

    try {
      // Use the absolute URL for the backend API during development
      const apiUrl = 'http://localhost:5000/api/command'; 
      const response = await fetch(apiUrl, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ command: command }),
      });

      const data = await response.json();

      if (!response.ok) {
        // Handle HTTP errors (e.g., 400, 500)
        throw new Error(data.message || `HTTP error! status: ${response.status}`);
      }

      setResult(data);
    } catch (e) {
      console.error("Failed to execute command:", e);
      setError(e.message || 'Failed to fetch');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <h2>macOS Command Runner</h2>
        <form onSubmit={handleSubmit} style={{ margin: '20px' }}>
          <input
            type="text"
            value={command}
            onChange={handleInputChange}
            placeholder="Enter command (e.g., ls -l)"
            style={{ padding: '10px', marginRight: '10px', width: '300px' }}
            disabled={isLoading}
          />
          <button type="submit" disabled={isLoading} style={{ padding: '10px' }}>
            {isLoading ? 'Running...' : 'Run Command'}
          </button>
        </form>

        {error && (
          <div style={{ color: 'red', marginTop: '15px' }}>
            <p>Error:</p>
            <pre>{error}</pre>
          </div>
        )}

        {result && (
          <div style={{ marginTop: '20px', textAlign: 'left', width: '80%', backgroundColor: '#282c34', padding: '15px', borderRadius: '5px' }}>
            <h4>Result for: <code style={{ color: '#61dafb' }}>{result.command}</code></h4>
            <p>Return Code: {result.returncode}</p>
            <h5>Stdout:</h5>
            <pre style={{ whiteSpace: 'pre-wrap', wordWrap: 'break-word', backgroundColor: '#3c4049', padding: '10px', borderRadius: '3px' }}>
              {result.stdout || '(empty)'}
            </pre>
            <h5>Stderr:</h5>
            <pre style={{ whiteSpace: 'pre-wrap', wordWrap: 'break-word', backgroundColor: '#3c4049', padding: '10px', borderRadius: '3px', color: '#ffcccb' }}>
              {result.stderr || '(empty)'}
            </pre>
          </div>
        )}
      </header>
    </div>
  );
}

export default App;
