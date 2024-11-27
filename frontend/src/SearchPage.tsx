import { ChangeEvent, FormEvent, useState } from 'react';

function SearchPage() {
  const [formData, setFormData] = useState({
    name_magazine: '',
    year: '',
    publisher: '',
    genre: '',
    article_title: '',
    article_author: '',
    article_page_range: '',
    content: '',
  });

  const handleChange = (e: ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { id, value } = e.target;
    setFormData((prevData) => ({
      ...prevData,
      [id]: value,
    }));
  };

  const handleSubmit = (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    console.log('Searching with data:', formData);
    // Effettua una richiesta API o altro per cercare articoli.
  };

  return (
    <div className="d-flex justify-content-center align-items-center vh-100">
      <div className="card bg-body-secondary p-4 shadow-sm" style={{ width: "50rem" }}>
        <h3 className="text-center mb-4">Search for an Article</h3>
        <form onSubmit={handleSubmit}>
          <div className="row">
            <div className="col-md-6 mb-3">
              <label htmlFor="name_magazine" className="form-label">Magazine Name</label>
              <input
                type="text"
                className="form-control"
                id="name_magazine"
                placeholder="Enter magazine name"
                value={formData.name_magazine}
                onChange={handleChange}
              />
            </div>
            <div className="col-md-6 mb-3">
              <label htmlFor="year" className="form-label">Year</label>
              <input
                type="number"
                className="form-control"
                id="year"
                placeholder="Enter year of publication"
                value={formData.year}
                onChange={handleChange}
              />
            </div>
          </div>
          <div className="row">
            <div className="col-md-6 mb-3">
              <label htmlFor="publisher" className="form-label">Publisher</label>
              <input
                type="text"
                className="form-control"
                id="publisher"
                placeholder="Enter publisher's name"
                value={formData.publisher}
                onChange={handleChange}
              />
            </div>
            <div className="col-md-6 mb-3">
              <label htmlFor="genre" className="form-label">Genre</label>
              <input
                type="text"
                className="form-control"
                id="genre"
                placeholder="Enter genre (e.g., Science)"
                value={formData.genre}
                onChange={handleChange}
              />
            </div>
          </div>
          <div className="row">
            <div className="col-md-6 mb-3">
              <label htmlFor="article_title" className="form-label">Article Title</label>
              <input
                type="text"
                className="form-control"
                id="article_title"
                placeholder="Enter article title"
                value={formData.article_title}
                onChange={handleChange}
              />
            </div>
            <div className="col-md-6 mb-3">
              <label htmlFor="article_author" className="form-label">Article Author</label>
              <input
                type="text"
                className="form-control"
                id="article_author"
                placeholder="Enter author's name"
                value={formData.article_author}
                onChange={handleChange}
              />
            </div>
          </div>
          <div className="row">
            <div className="col-md-6 mb-3">
              <label htmlFor="article_page_range" className="form-label">Article Page Range</label>
              <input
                type="text"
                className="form-control"
                id="article_page_range"
                placeholder="Enter page range (e.g., 1-10)"
                value={formData.article_page_range}
                onChange={handleChange}
              />
            </div>
            <div className="col-md-6 mb-3">
              <label htmlFor="content" className="form-label">Content</label>
              <textarea
                className="form-control"
                id="content"
                rows={3}
                placeholder="Enter article content"
                value={formData.content}
                onChange={handleChange}
              ></textarea>
            </div>
          </div>
          <button type="submit" className="btn btn-primary w-100">
            Search
          </button>
        </form>
      </div>
    </div>
  );
}

export default SearchPage;
