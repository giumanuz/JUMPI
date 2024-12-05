import React, { useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import FormTemplate from './FormTemplate';

const EditPage = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const initialData = location.state?.data || {};

  const [formData, setFormData] = useState(initialData);

  const handleChange = (field: string, value: any) => {
    setFormData((prev) => ({ ...prev, [field]: value }));
  };

  const handleImageChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      const reader = new FileReader();
      reader.onloadend = () => {
        setFormData((prev) => ({ ...prev, image: reader.result }));
      };
      reader.readAsDataURL(file);
    }
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    console.log('Updated Data:', formData);
    navigate(-1); // Torna alla pagina precedente
  };

  return (
    <FormTemplate
      title="Edit Magazine"
      onSubmit={handleSubmit}
      button={<button type="submit" className="btn btn-primary w-100">Save</button>}
    >
      {[
        <div className="mb-3">
          <label htmlFor="name" className="form-label">Name</label>
          <input
            id="name"
            className="form-control"
            value={formData.name || ''}
            onChange={(e) => handleChange('name', e.target.value)}
          />
        </div>,
        <div className="mb-3">
          <label htmlFor="year" className="form-label">Year</label>
          <input
            id="year"
            type="number"
            className="form-control"
            value={formData.year || ''}
            onChange={(e) => handleChange('year', e.target.value)}
          />
        </div>,
        <div className="mb-3">
          <label htmlFor="publisher" className="form-label">Publisher</label>
          <input
            id="publisher"
            className="form-control"
            value={formData.publisher || ''}
            onChange={(e) => handleChange('publisher', e.target.value)}
          />
        </div>,
        <div className="mb-3">
          <label htmlFor="genre" className="form-label">Genre</label>
          <input
            id="genre"
            className="form-control"
            value={formData.genre || ''}
            onChange={(e) => handleChange('genre', e.target.value)}
          />
        </div>,
        <div className="mb-3">
          <label htmlFor="articleTitle" className="form-label">First Article Title</label>
          <input
            id="articleTitle"
            className="form-control"
            value={formData.articles?.[0]?.title || ''}
            onChange={(e) =>
              handleChange('articles', [
                { ...formData.articles?.[0], title: e.target.value },
              ])
            }
          />
        </div>,
        <div className="mb-3">
          <label htmlFor="image" className="form-label">Image</label>
          <div className="mb-2">
            <img
              src={formData.image || 'https://via.placeholder.com/150'}
              alt="Magazine"
              className="img-fluid rounded"
              style={{ maxHeight: '150px' }}
            />
          </div>
        </div>
      ]}
    </FormTemplate>
  );
};

export default EditPage;
