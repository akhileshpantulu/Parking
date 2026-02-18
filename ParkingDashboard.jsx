async function handleSearch() {
  setLoading(true);
  try {
    // This fetches the JSON file created by your Python script
    const response = await fetch("./parking_data.json"); 
    const data = await response.json();
    setResults(data);
  } catch (e) {
    setError("Could not load latest parking data.");
  } finally {
    setLoading(false);
  }
}
