import { Link } from 'react-router-dom';

function HomePage() {
  return (
    <div className="d-flex flex-column min-vh-100">
      <div className="m-auto">
        <h1 className="text-center mb-4">JUMPI</h1>
        <div className="d-flex gap-2">
          <Link to="/search" className="btn btn-primary btn-lg mx-auto">
            Search
          </Link>
          <Link to="/upload" className="btn btn-primary btn-lg mx-auto">
            Upload
          </Link>
        </div>
      </div>
    </div>
  );
}

export default HomePage;