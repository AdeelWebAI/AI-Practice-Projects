import Agent from "./components/Agent";

export default function App() {
  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gray-100 p-4">
      <h1 className="text-3xl font-bold text-gray-800 mb-6">
        Weather Checker App
      </h1>
      <Agent />
    </div>
  );
}
