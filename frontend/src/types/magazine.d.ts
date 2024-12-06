type Magazine = {
  id: string;
  name: string;
  date: Date;
  publisher: string;
  edition?: string;
  abstract?: string;
  genres: string[];
  categories: string[];
  createdOn: Date;
  editedOn: Date;
};
