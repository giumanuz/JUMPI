import { useLocation } from "react-router-dom";
import ArticleCard from "../components/ArticleCard";

const QueryResultPage = () => {
  const location = useLocation();
  const results = location.state?.results ?? [];

  return (
    <div className="container mt-4">
      <h1>Search Results</h1>
      {results.length === 0 ? (
        <p>No results found.</p>
      ) : (
        <div className="row">
          {results.map((result: any) => (
            <div className="col-md-4 mb-3" key={result._id}>
              <ArticleCard
                article={{
                  id: result._id,
                  title: result._source.title,
                  author: result._source.author,
                  content: result._source.content,
                  createdOn: result._source.created_on.toDate(),
                }}
                onShowDetails={() => {}}
              />
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default QueryResultPage;
