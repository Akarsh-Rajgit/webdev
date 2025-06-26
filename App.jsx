import React, { useEffect, useState } from 'react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, LineChart, Line, CartesianGrid, Legend, ResponsiveContainer } from 'recharts';
import PropertyForm from './components/propertyForm';
import FilterBar from './components/FilterBar';
import PropertyTable from './components/PropertyTable';
import Charts from './components/Charts';

function App() {
  const [properties, setProperties] = useState([]);
  const [filtered, setFiltered] = useState([]);
  const [formData, setFormData] = useState({
    location: '',
    size: '',
    total_sqft: '',
    bath: '',
    price_lakhs: '',
    price_per_sqft: '',
  });
  const [filters, setFilters] = useState({
    location: '',
    size: '',
    total_sqft: '',
    price_per_sqft: '',
  });

  useEffect(() => {
    fetchProperties();
  }, []);

  const fetchProperties = async () => {
    try {
      const response = await fetch('http://127.0.0.1:5000/properties');
      const data = await response.json();
      setProperties(data);
      setFiltered(applyFilters(data, filters).slice(0, 50));
    } catch (error) {
      console.error('Error fetching properties:', error);
    }
  };

  const handleDelete = async (id) => {
    try {
      await fetch(`http://127.0.0.1:5000/properties/${id}`, {
        method: 'DELETE',
      });
      fetchProperties();
    } catch (error) {
      console.error('Error deleting property:', error);
    }
  };

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await fetch('http://127.0.0.1:5000/properties', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData),
      });
      setFormData({
        location: '',
        size: '',
        total_sqft: '',
        bath: '',
        price_lakhs: '',
        price_per_sqft: '',
      });
      fetchProperties();
    } catch (error) {
      console.error('Error adding property:', error);
    }
  };

  const applyFilters = (properties, filters) => {
    return properties.filter((prop) =>
      (filters.location === '' || prop.location.toLowerCase().includes(filters.location.toLowerCase())) &&
      (filters.size === '' || prop.size.toLowerCase().includes(filters.size.toLowerCase())) &&
      (filters.total_sqft === '' || parseFloat(prop.total_sqft) >= parseFloat(filters.total_sqft)) &&
      (filters.price_per_sqft === '' || parseFloat(prop.price_per_sqft) <= parseFloat(filters.price_per_sqft))
    );
  };

  const handleFilterChange = (e) => {
    const newFilters = { ...filters, [e.target.name]: e.target.value };
    setFilters(newFilters);
    const filteredProps = applyFilters(properties, newFilters);
    setFiltered(filteredProps.slice(0, 50));
  };

  const locationStats = {};
  properties.forEach(p => {
    if (!locationStats[p.location]) {
      locationStats[p.location] = { count: 0, total: 0 };
    }
    locationStats[p.location].count += 1;
    locationStats[p.location].total += parseFloat(p.price_per_sqft);
  });
  const avgPricePerLocation = Object.entries(locationStats).map(([loc, data]) => ({
    location: loc,
    avgPricePerSqft: (data.total / data.count).toFixed(2)
  }));

  const priceTrendData = properties
    .sort((a, b) => parseFloat(a.price_per_sqft) - parseFloat(b.price_per_sqft))
    .slice(0, 20)
    .map((p, index) => ({
      index,
      price_per_sqft: parseFloat(p.price_per_sqft)
    }));

  return (
    <div style={{ padding: '20px', fontFamily: 'Arial, sans-serif', backgroundColor: '#1e1e1e', color: '#fff', minHeight: '100vh' }}>
      <h1>🏠 Real Estate Survey</h1>

      <h2> Map View</h2>

      <div style={{ maxWidth: "800px", margin: "auto" }}>
  <img
    src="/map_blore.png"
    alt="Bangalore Map"
    style={{ width: "100%", maxHeight: "300px", objectFit: "cover", borderRadius: "12px" }}
  />
</div>

      <h2 class = 'stat'>Property Statistics:</h2>

      <Charts avgPricePerLocation={avgPricePerLocation} priceTrendData={priceTrendData} />

      <h2> Add Property:</h2>

      <PropertyForm formData={formData} onChange={handleChange} onSubmit={handleSubmit} />

      <h2> Search Properties:</h2>
      <FilterBar filters={filters} onChange={handleFilterChange} />

      <PropertyTable properties={filtered} onDelete={handleDelete} />
    </div>
  );
}

export default App;