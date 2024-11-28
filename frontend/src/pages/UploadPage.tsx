import {ChangeEvent, FormEvent, useState} from 'react';
import InputField from '../components/InputField';
import axios from 'axios';
import {useNavigate} from 'react-router-dom';
import FormBasePage from "./FormPageBase.tsx";

const UploadPage = () => {
  const [formData, setFormData] = useState({
    name_magazine: '',
    year: '',
    publisher: '',
    genre: '',
    article_title: '',
    article_author: '',
    article_page_range: '',
    document: null as File | null,
  });

  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleChange = (e: ChangeEvent<HTMLInputElement>) => {
    const {id, value, files} = e.target;
    setFormData((prevData) => ({
      ...prevData,
      [id]: files ? files[0] : value,
    }));
  };

  const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    if (!formData.document) {
      alert('Please upload a document.');
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
      uploadData.append('files', formData.document);

      const response = await axios.post('http://localhost:5123/analyze-documents', uploadData, {
        headers: {'Content-Type': 'multipart/form-data'},
      });

      // Navigate to the result page with the data from the response
      navigate('/result', {state: response.data});
    } catch (error) {
      console.error('Error uploading document:', error);
      alert('Failed to analyze document. Please try again.');
    } finally {
      setLoading(false); // Stop loading
    }
  };

  return (
    <FormBasePage
      title={"Search for an article"}
      button={
        <button type="submit" className="btn btn-primary w-100">
          Search
        </button>
      }
      onSubmit={handleSubmit}
      loading={loading}
      loadingDescription={"Uploading document..."}
    >
      <InputField
        id="name_magazine"
        label="Magazine Name"
        placeholder="Enter magazine name"
        value={formData.name_magazine}
        onChange={handleChange}
      />
      <InputField
        id="year"
        label="Year"
        placeholder="Enter year of publication"
        value={formData.year}
        onChange={handleChange}
        type="number"
      />
      <InputField
        id="publisher"
        label="Publisher"
        placeholder="Enter publisher's name"
        value={formData.publisher}
        onChange={handleChange}
      />
      <InputField
        id="genre"
        label="Genre"
        placeholder="Enter genre (e.g., Science)"
        value={formData.genre}
        onChange={handleChange}
      />
      <InputField
        id="article_title"
        label="Article Title"
        placeholder="Enter article title"
        value={formData.article_title}
        onChange={handleChange}
      />
      <InputField
        id="article_author"
        label="Article Author"
        placeholder="Enter author's name"
        value={formData.article_author}
        onChange={handleChange}
      />
      <InputField
        id="article_page_range"
        label="Article Page Range"
        placeholder="Enter page range (e.g., 1-10)"
        value={formData.article_page_range}
        onChange={handleChange}
      />
      <div className="mb-3">
        <label htmlFor="document" className="form-label">
          Upload Document (Image or PDF)
        </label>
        <input
          type="file"
          className="form-control"
          id="document"
          accept="image/png, image/jpeg, .pdf"
          onChange={handleChange}
        />
      </div>
    </FormBasePage>
  );
};

export default UploadPage;
