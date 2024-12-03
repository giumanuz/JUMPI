import {ChangeEvent, FormEvent, useState} from 'react';
import InputField from '../components/InputField';
import TextAreaField from '../components/TextAreaField';
import FormTemplate from "./FormTemplate.tsx";
import {useNavigate} from "react-router-dom";
import axiosInstance from "../axiosInstance.ts";
import {AxiosError} from "axios";

const SearchPage = () => {
  const [params, setParams] = useState({
    name_magazine: '',
    year: '',
    publisher: '',
    genre: '',
    article_title: '',
    article_author: '',
    content: '',
  });
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const onChange = (e: ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const {id, value} = e.target;
    setParams((prevData) => ({
      ...prevData,
      [id]: value,
    }));
  };

  const onSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setLoading(true);

    try {
      const response = await axiosInstance.get(`/query`, {params});
      navigate('/queryResults', {state: {results: response.data}});
      console.log(response)
    } catch (error) {
      const axiosError = error as AxiosError;
      console.error('Error uploading documents:', error);
      const data = axiosError?.response?.data as {error?: string};
      const text = data.error;
      console.error('Error uploading document:', error);
      alert(`Failed to analyze document: ${text}`);
    } finally {
      setLoading(false); // Stop loading
    }
  };

  return (
    <FormTemplate
      title={"Search for an article"}
      loading={loading}
      button={
        <button type="submit" className="btn btn-primary w-100">
          Search
        </button>
      }
      onSubmit={onSubmit}
    >
      <InputField
        id="name_magazine"
        label="Magazine Name"
        placeholder="Enter magazine name"
        value={params.name_magazine}
        onChange={onChange}
      />
      <InputField
        id="year"
        label="Year"
        placeholder="Enter year of publication"
        value={params.year}
        onChange={onChange}
        type="number"
      />
      <InputField
        id="publisher"
        label="Publisher"
        placeholder="Enter publisher's name"
        value={params.publisher}
        onChange={onChange}
      />
      <InputField
        id="genre"
        label="Genre"
        placeholder="Enter genre (e.g., Science)"
        value={params.genre}
        onChange={onChange}
      />
      <InputField
        id="article_title"
        label="Article Title"
        placeholder="Enter article title"
        value={params.article_title}
        onChange={onChange}
      />
      <InputField
        id="article_author"
        label="Article Author"
        placeholder="Enter author's name"
        value={params.article_author}
        onChange={onChange}
      />
      <TextAreaField
        id="content"
        label="Content"
        placeholder="Enter article content"
        value={params.content}
        onChange={onChange}
      />
    </FormTemplate>
  )
};

export default SearchPage;
