import React from "react";
import "../styles/Home.css"

const StaffCard = ({staff}) => {
  localStorage.setItem("staff_id", staff.id);
  return (
    <div className="staff-card">
      <img
        src={staff.image}
        alt={staff.user.username}
        className="w-full h-32 object-cover rounded-t-lg"
      />
      <h2 className="text-xl font-semibold mt-2">{staff.user.first_name} {staff.user.last_name}</h2>
      <p className="text-gray-600">Roles: {staff.role}</p>
      <p className="text-gray-600">Department: {staff.department}</p>
    </div>
  );
}

export default StaffCard;