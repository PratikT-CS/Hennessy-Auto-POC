import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.jsx'
import { Router, RouterProvider, createBrowserRouter } from 'react-router-dom'
import DealForm from './components/DealForm'
import DealDetails from './components/DealDetails'
import Error from './components/Error'

const appRouter = createBrowserRouter([
  {
    path: '/',
    element: <App />,
    errorElement: <Error />,
    children: [
      {
        path: '/',
        element: <DealForm />
      },
      {
        path: '/deal/:dealId',
        element: <DealDetails />
      }
    ]
  }
])

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <RouterProvider router={appRouter} />
  </StrictMode>,
)
