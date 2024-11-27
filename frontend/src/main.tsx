import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.scss'
import UploadPage from "./UploadPage.tsx";

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    {/*<App />*/}
    {/*<SearchPage />*/}
    <UploadPage />
  </StrictMode>,
)
