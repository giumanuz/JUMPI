function SearchPage() {
  return (
    <div
      className="d-flex justify-content-center align-items-center vh-100"
    >
      <div className="card bg-body-secondary p-4 shadow-sm" style={{ width: "30rem" }}>
        <h3 className="text-center mb-4">Search for an Article</h3>
        <form>
          <div className="mb-3">
            <label htmlFor="title" className="form-label">
              Title
            </label>
            <input
              type="text"
              className="form-control"
              id="title"
              placeholder="Enter article title"
            />
          </div>
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
            <label htmlFor="content" className="form-label">
              Content
            </label>
            <textarea
              className="form-control"
              id="content"
              rows={3}
              placeholder="Enter article content"
            ></textarea>
          </div>
          <button  className="btn btn-primary w-100"
          >
            Search
          </button>
        </form>
      </div>
    </div>
  );
}

export default SearchPage;