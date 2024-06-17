
const  monthNames= [
    'Января', 'Февраля', 'Марта', 'Апреля', 'Мая', 'Июня',
    'Июля', 'Августа', 'Сентября', 'Октября', 'Ноября', 'Декабря'
  ]
function dateToString(date) {
    const day = date.getDate();
    const month = date.getMonth();
    const monthName = monthNames[month];
    return {'day':day, 'month':monthName};
}

export default dateToString;