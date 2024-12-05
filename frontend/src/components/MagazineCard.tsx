import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

const MagazineCard = ({ data }: { data: any }) => {
  const navigate = useNavigate();

  if (!data || !data._id) {
    console.error('Missing _id in data passed to MagazineCard:', data);
    return null;
  }

  const { _id, name, year, publisher, genre, articles } = data;
  const article = articles?.[0];
  const [isExpanded, setIsExpanded] = useState(false);

  const toggleExpand = () => {
    setIsExpanded((prev) => !prev);
  };

  const handleEdit = () => {
    navigate(`/edit/${_id}`, { state: { data } });
  };

  return (
    <div className="card mb-3 position-relative">
      <button
        className="btn btn-sm btn-outline-secondary position-absolute top-0 end-0 m-2"
        onClick={handleEdit}
        title="Edit"
      >
        ✏️
      </button>
      <div className="card-header">
        <h5>{name}</h5>
        <small className="text-muted">
          {year} | {publisher} | {genre}
        </small>
      </div>
      <div className="card-body">
        {article ? (
          <>
            <h6 className="card-title">{article.title}</h6>
            <p className="card-subtitle text-muted mb-3">Author: {article.author}</p>
            <p className="card-text">
              {isExpanded ? article.content : `${article.content?.substring(0, 400)}...`}
            </p>
            <button className="btn btn-link p-0" onClick={toggleExpand}>
              {isExpanded ? 'Collapse' : 'Read more'}
            </button>
          </>
        ) : (
          <p className="text-muted">No articles available.</p>
        )}
      </div>
    </div>
  );
};

export default MagazineCard;
