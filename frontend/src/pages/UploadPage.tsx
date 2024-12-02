import { ChangeEvent, FormEvent, useState } from 'react';
import InputField from '../components/InputField';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import FormTemplate from './FormTemplate.tsx';

const UploadPage = () => {
  const [formData, setFormData] = useState({
    name_magazine: '',
    year: '',
    publisher: '',
    genre: '',
    article_title: '',
    article_author: '',
    article_page_range: '',
    documents: [] as File[],
  });

  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const onChange = (e: ChangeEvent<HTMLInputElement>) => {
    const { id, value, files } = e.target;

    setFormData((prevData) => ({
      ...prevData,
      [id]: files ? Array.from(files) : value,
    }));
  };

  const onSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    if (!formData.documents.length) {
      alert('Please upload at least one document.');
      return;
    }

    setLoading(true);

    try {
      const metadata = JSON.stringify({
        name_magazine: formData.name_magazine,
        year: formData.year,
        publisher: formData.publisher,
        genre: formData.genre,
        article_title: formData.article_title,
        article_author: formData.article_author,
        article_page_range: formData.article_page_range,
      });

      const uploadData = new FormData();
      uploadData.append('metadata', metadata);

      formData.documents.forEach((file) => {
        uploadData.append('files', file);
      });

      const url = import.meta.env.VITE_API_ENDPOINT;
      const response = await axios.post(`${url}/analyze-documents`, uploadData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });

      navigate('/result', { state: response.data });
    } catch (error) {
      console.error('Error uploading documents:', error);
      alert('Failed to analyze documents. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <FormTemplate
      title="Upload an article"
      button={
        <button type="submit" className="btn btn-success w-100">
          Upload
        </button>
      }
      onSubmit={onSubmit}
      loading={loading}
      loadingDescription="Uploading documents..."
    >
      <InputField
        id="name_magazine"
        label="Magazine Name"
        placeholder="Enter magazine name"
        value={formData.name_magazine}
        onChange={onChange}
      />
      <InputField
        id="year"
        label="Year"
        placeholder="Enter year of publication"
        value={formData.year}
        onChange={onChange}
        type="number"
      />
      <InputField
        id="publisher"
        label="Publisher"
        placeholder="Enter publisher's name"
        value={formData.publisher}
        onChange={onChange}
      />
      <InputField
        id="genre"
        label="Genre"
        placeholder="Enter genre (e.g., Science)"
        value={formData.genre}
        onChange={onChange}
      />
      <InputField
        id="article_title"
        label="Article Title"
        placeholder="Enter article title"
        value={formData.article_title}
        onChange={onChange}
      />
      <InputField
        id="article_author"
        label="Article Author"
        placeholder="Enter author's name"
        value={formData.article_author}
        onChange={onChange}
      />
      <InputField
        id="article_page_range"
        label="Article Page Range"
        placeholder="Enter page range (e.g., 1-10)"
        value={formData.article_page_range}
        onChange={onChange}
      />
      <div className="mb-3">
        <label htmlFor="documents" className="form-label">
          Upload Documents (Images or PDFs)
        </label>
        <input
          type="file"
          className="form-control"
          id="documents"
          accept="image/png, image/jpeg, .pdf"
          multiple
          onChange={onChange}
        />
      </div>
    </FormTemplate>
  );
};

export default UploadPage;
