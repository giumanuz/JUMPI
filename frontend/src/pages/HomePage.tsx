import {Link} from 'react-router-dom';
import {useState} from "react";
import axiosInstance from "../axiosInstance.ts";

function HomePage() {
  const [apiKey, setApiKey] = useState('');

  const updateApiKey = () => {
    axiosInstance.defaults.headers.common['X-API-KEY'] = apiKey;
  }

  return (
    <div className="d-flex flex-column min-vh-100">
      <div className="m-auto">
        <h1 className="text-center mb-4">JUMPI</h1>
        <div className="d-flex gap-2">
          <Link to="/search" className="btn btn-primary btn-lg mx-auto" onClick={updateApiKey}>
            Search
          </Link>
          <Link to="/upload" className="btn btn-primary btn-lg mx-auto" onClick={updateApiKey}>
            Upload
          </Link>
        </div>
        <div className="mt-4">
          <label htmlFor="apiKey" className="form-label">API Key:</label>
          <input type="password" id="apiKey" className="form-control" placeholder="Enter your API key"
                 onChange={(e) => setApiKey(e.target.value)} value={apiKey}
          />
        </div>
      </div>
    </div>
  );
}

export default HomePage;