function SearchPage() {
  return (
    <div
      className="d-flex justify-content-center align-items-center vh-100"
    >
      <div className="card bg-body-secondary p-4 shadow-sm" style={{ width: "30rem" }}>
        <h3 className="text-center mb-4">Create a New Article</h3>
        <form>
          <div className="mb-3">
            <label htmlFor="author" className="form-label">
              Author
            </label>
            <input
              type="text"
              className="form-control"
              id="author"
              placeholder="Enter author's name"
            />
          </div>
          <div className="mb-3">
            <label htmlFor="year" className="form-label">
              Year
            </label>
            <input
              type="number"
              className="form-control"
              id="year"
              placeholder="Enter year of publication"
            />
          </div>
          <div className="mb-3">
            <label htmlFor="document" className="form-label">
              Upload Document (Image or PDF)
            </label>
            <input
              type="file"
              className="form-control"
              id="document"
              accept="image/png, image/jpeg, .pdf"
            />
          </div>
          <button type="submit" className="btn btn-success w-100">
            Create Article
          </button>
        </form>
      </div>
    </div>
  );
}

export default SearchPage;