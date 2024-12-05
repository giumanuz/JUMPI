// src/pages/UploadArticlePage.tsx

import { useState } from 'react';
import { useSearchParams, useNavigate } from 'react-router-dom';
import axiosInstance from '../axiosInstance';
import FormTemplate from '../pages/FormTemplate';

function UploadArticlePage() {
  const [searchParams] = useSearchParams();
  const magazine_id = searchParams.get('magazine_id');
  const navigate = useNavigate();

  const [title, setTitle] = useState('');
  const [author, setAuthor] = useState('');
  const [pageRange, setPageRange] = useState('');
  const [images, setImages] = useState<FileList | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [successMessage, setSuccessMessage] = useState<string | null>(null);

  const handleImageChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
      setImages(e.target.files);
    }
  };

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    if (!magazine_id) {
      setError('Magazine ID is missing.');
      return;
    }

    const pageRangeRegex = /^\d+-\d+$/;
    if (!pageRangeRegex.test(pageRange)) {
      setError('Page Range must be in the format "start-end", e.g., "1-5".');
      return;
    }

    const formData = new FormData();
    formData.append('title', title);
    formData.append('author', author);
    formData.append('page_range', pageRange);
    formData.append('magazine_id', magazine_id);

    if (images) {
      Array.from(images).forEach((image) => {
        formData.append('images', image);
      });
    }

    try {
      const res = await axiosInstance.post('/uploadArticle', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      if (res.data.status === 'ok') {
        const { extracted_text, image_comparisons } = res.data.article;
        navigate('/resultPage', { state: { extracted_text, image_comparisons } });
      } else {
        setError('Failed to upload the article. Please try again.');
      }
    } catch (err) {
      console.error('Error uploading article:', err);
      setError('Failed to upload the article. Please try again.');
    }
  };

  return (
    <FormTemplate
      title="Upload Article"
      onSubmit={handleSubmit}
      button={
        <button type="submit" className="btn btn-primary mt-3">
          Submit
        </button>
      }
    >
      {error && <div className="alert alert-danger">{error}</div>}
      {successMessage && <div className="alert alert-success">{successMessage}</div>}
      <div className="mb-3">
        <label className="form-label">Title</label>
        <input
          type="text"
          className="form-control"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          required
        />
      </div>
      <div className="mb-3">
        <label className="form-label">Author</label>
        <input
          type="text"
          className="form-control"
          value={author}
          onChange={(e) => setAuthor(e.target.value)}
          required
        />
      </div>
      <div className="mb-3">
        <label className="form-label">Page Range (e.g., "1-5")</label>
        <input
          type="text"
          className="form-control"
          value={pageRange}
          onChange={(e) => setPageRange(e.target.value)}
          placeholder="e.g., 1-5"
          required
        />
      </div>
      <div className="mb-3">
        <label className="form-label">Upload Images</label>
        <input
          type="file"
          className="form-control"
          multiple
          accept="image/*"
          onChange={handleImageChange}
        />
      </div>
    </FormTemplate>
  );
}

export default UploadArticlePage;
