import React, { useState } from 'react';
import axios from 'axios';

function LearningRequestForm() {
  const [input, setInput] = useState('');

  const handleSubmit = async (event) => {
    event.preventDefault();
    try {
      const response = await axios.post('http://localhost:8000/api/learning-request', { input });
      console.log('Server response:', response.data);
    } catch (error) {
      console.error('There was an error sending the request!', error);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <label>
        Enter your learning request:
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
        />
      </label>
      <button type="submit">Submit</button>
    </form>
  );
}

export default LearningRequestForm;
