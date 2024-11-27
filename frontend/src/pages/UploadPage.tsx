function UploadPage() {
  return (
    <div className="d-flex justify-content-center align-items-center vh-100">
      <div className="card bg-body-secondary p-4 shadow-sm" style={{ width: "50rem" }}>
        <h3 className="text-center mb-4">Upload a New Article</h3>
        <form>
          <div className="row">
            <div className="col-md-6 mb-3">
              <label htmlFor="name_magazine" className="form-label">
                Magazine Name
              </label>
              <input
                type="text"
                className="form-control"
                id="name_magazine"
                placeholder="Enter magazine name"
              />
            </div>
            <div className="col-md-6 mb-3">
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
          </div>
          <div className="row">
            <div className="col-md-6 mb-3">
              <label htmlFor="publisher" className="form-label">
                Publisher
              </label>
              <input
                type="text"
                className="form-control"
                id="publisher"
                placeholder="Enter publisher's name"
              />
            </div>
            <div className="col-md-6 mb-3">
              <label htmlFor="genre" className="form-label">
                Genre
              </label>
              <input
                type="text"
                className="form-control"
                id="genre"
                placeholder="Enter genre (e.g., Science)"
              />
            </div>
          </div>
          <div className="row">
            <div className="col-md-6 mb-3">
              <label htmlFor="article_title" className="form-label">
                Article Title
              </label>
              <input
                type="text"
                className="form-control"
                id="article_title"
                placeholder="Enter article title"
              />
            </div>
            <div className="col-md-6 mb-3">
              <label htmlFor="article_author" className="form-label">
                Article Author
              </label>
              <input
                type="text"
                className="form-control"
                id="article_author"
                placeholder="Enter author's name"
              />
            </div>
          </div>
          <div className="row">
            <div className="col-md-6 mb-3">
              <label htmlFor="article_page_range" className="form-label">
                Article Page Range
              </label>
              <input
                type="text"
                className="form-control"
                id="article_page_range"
                placeholder="Enter page range (e.g., 1-10)"
              />
            </div>
            <div className="col-md-6 mb-3">
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
          </div>
          <button type="submit" className="btn btn-success w-100">
            Upload Article
          </button>
        </form>
      </div>
    </div>
  );
}

export default UploadPage;
