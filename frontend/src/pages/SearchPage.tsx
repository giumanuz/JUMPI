import {ChangeEvent, FormEvent, useState} from 'react';
import InputField from '../components/InputField';
import TextAreaField from '../components/TextAreaField';
import FormBasePage from "./FormPageBase.tsx";

const SearchPage = () => {
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
    const {id, value} = e.target;
    setFormData((prevData) => ({
      ...prevData,
      [id]: value,
    }));
  };

  const handleSubmit = (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    console.log('Searching with data:', formData);
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
      <TextAreaField
        id="content"
        label="Content"
        placeholder="Enter article content"
        value={formData.content}
        onChange={handleChange}
      />
    </FormBasePage>
  )
};

export default SearchPage;
