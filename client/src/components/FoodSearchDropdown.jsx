export default function FoodSearchDropdown({ foods, value, onChange }) {
  return (
    <select value={value} onChange={(e) => onChange(Number(e.target.value))}>
      {foods.map((food) => (
        <option key={food.id} value={food.id}>
          {food.name} ({food.category})
        </option>
      ))}
    </select>
  );
}

