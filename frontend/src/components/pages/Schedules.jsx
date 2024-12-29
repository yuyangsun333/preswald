import React, { useState } from 'react';

const Schedules = () => {
  const [schedules, setSchedules] = useState([]);
  const [formData, setFormData] = useState({
    frequency: '1',
    interval: 'Week(s)',
    startDate: '',
    time: '',
    timezone: 'Los Angeles (PST)',
  });

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleFormSubmit = (e) => {
    e.preventDefault();
    setSchedules((prevSchedules) => [
      ...prevSchedules,
      { ...formData, id: Date.now() },
    ]);
    setFormData({
      frequency: '1',
      interval: 'Week(s)',
      startDate: '',
      time: '',
      timezone: 'Los Angeles (PST)',
    });
  };

  const handleDelete = (id) => {
    setSchedules(schedules.filter((schedule) => schedule.id !== id));
  };

  return (
    <div className="p-5 pl-5 font-sans text-gray-800 max-w-4xl pl-0 text-left">
      <h1 className="text-2xl font-bold mb-4">Schedules</h1>

      {/* Schedule Creation Form */}
      <form onSubmit={handleFormSubmit} className="mb-5">
        <h2 className="text-lg font-medium mb-3">Create a Schedule</h2>

        <div className="mb-4">
          <label className="block text-sm font-medium mb-1">Run every:</label>
          <div className="grid grid-cols-2 gap-2">
            <input
              type="number"
              name="frequency"
              value={formData.frequency}
              onChange={handleInputChange}
              className="p-2 border border-gray-300 rounded"
            />
            <select
              name="interval"
              value={formData.interval}
              onChange={handleInputChange}
              className="p-2 border border-gray-300 rounded"
            >
              <option value="Day(s)">Day(s)</option>
              <option value="Week(s)">Week(s)</option>
              <option value="Month(s)">Month(s)</option>
            </select>
          </div>
        </div>

        <div className="mb-4">
          <label className="block text-sm font-medium mb-1">Start Date:</label>
          <input
            type="date"
            name="startDate"
            value={formData.startDate}
            onChange={handleInputChange}
            className="p-2 border border-gray-300 rounded w-full"
          />
        </div>

        <div className="mb-4">
          <label className="block text-sm font-medium mb-1">Time:</label>
          <input
            type="time"
            name="time"
            value={formData.time}
            onChange={handleInputChange}
            className="p-2 border border-gray-300 rounded w-full"
          />
        </div>

        <div className="mb-4">
          <label className="block text-sm font-medium mb-1">Timezone:</label>
          <select
            name="timezone"
            value={formData.timezone}
            onChange={handleInputChange}
            className="p-2 border border-gray-300 rounded w-full"
          >
            <option value="Los Angeles (PST)">Los Angeles (PST)</option>
            <option value="New York (EST)">New York (EST)</option>
            <option value="London (GMT)">London (GMT)</option>
            <option value="Tokyo (JST)">Tokyo (JST)</option>
          </select>
        </div>

        <button
          type="submit"
          className="px-4 py-2 text-white bg-blue-500 rounded hover:bg-blue-600"
        >
          Add Schedule
        </button>
      </form>

      {/* Schedule List */}
      <table className="w-full text-left text-sm">
        <thead>
          <tr>
            <th className="p-3 text-left">Frequency</th>
            <th className="p-3 text-left">Start Date</th>
            <th className="p-3 text-left">Time</th>
            <th className="p-3 text-left">Timezone</th>
            <th className="p-3 text-left">Actions</th>
          </tr>
        </thead>
        <tbody>
          {schedules.map((schedule) => (
            <tr key={schedule.id}>
              <td className="p-3 text-left">
                Every {schedule.frequency} {schedule.interval}
              </td>
              <td className="p-3 text-left">{schedule.startDate}</td>
              <td className="p-3 text-left">{schedule.time}</td>
              <td className="p-3 text-left">{schedule.timezone}</td>
              <td className="p-3 text-left">
                <button
                  onClick={() => handleDelete(schedule.id)}
                  className="px-3 py-1 text-white bg-red-500 rounded hover:bg-red-600"
                >
                  Delete
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default Schedules;
