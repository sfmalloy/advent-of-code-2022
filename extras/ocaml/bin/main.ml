open Solve

let days = [
  Day01.run;
  Day02.run
]

let () =
  Printf.printf "Day (1-%d): " (List.length days);
  let day_num = read_int () in
  List.nth days (day_num - 1) ();;
;;
