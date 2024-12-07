import React, { useState } from "react";

interface Article {
  title: string;
  author: string;
  content: string;
}

interface MagazineData {
  _id: string;
  name: string;
  year: string;
  publisher: string;
  genre: string;
  articles: Article[];
}

interface MagazineCardProps {
  data: MagazineData;
  onEdit: (id: string) => void;
}

const MagazineCard: React.FC<MagazineCardProps> = ({ data, onEdit }) => {
  if (!data || !data._id) {
    console.error("Missing _id in data passed to MagazineCard:", data);
    return null;
  }

  const { _id, name, year, publisher, genre, articles } = data;
  const article = articles?.[0];
  const [isExpanded, setIsExpanded] = useState(false);

  const toggleExpand = () => {
    setIsExpanded((prev) => !prev);
  };

  const handleEditClick = () => {
    onEdit(_id);
  };

  return (
    <div className="card mb-3 h-100 d-flex flex-column p-3">
      <div className="mb-3">
        <h5>{name}</h5>
        <small className="text-muted">
          {year} | {publisher} | {genre}
        </small>
      </div>

      <div className="mb-3 flex-grow-1">
        {article ? (
          <>
            <h6 className="card-title">{article.title}</h6>
            <p className="card-subtitle text-muted mb-3">
              Author: {article.author}
            </p>
            <p className="card-text">
              {isExpanded
                ? article.content
                : `${article.content?.substring(0, 400)}...`}
            </p>
            <button className="btn btn-link p-0" onClick={toggleExpand}>
              {isExpanded ? "Collapse" : "Read more"}
            </button>
          </>
        ) : (
          <p className="text-muted">No articles available.</p>
        )}
      </div>

      <div className="mt-auto">
        <button
          className="btn btn-primary"
          onClick={handleEditClick}
        >
          Edit Article
        </button>
      </div>
    </div>
  );
};

export default MagazineCard;
