let read_elves filename =
  let file = open_in filename in
  let rec read prev =
    try
      let line = input_line file in
      match int_of_string_opt (String.trim line) with
      | None -> prev :: read 0
      | Some x -> read (x + prev)
    with End_of_file -> []
  in
  read 0
;;

let rec print_list lst =
  match lst with
  | [] -> ()
  | hd::tl -> let () = Printf.printf "%d\n" hd in print_list tl
;;

let list_max lst =
  let rec find curr l =
    match l with
    | hd::tl when hd > curr -> find hd tl
    | _::tl -> find curr tl
    | [] -> curr
  in
  find 0 lst
;;

let top_three lst =
  let rec find a b c l =
    match l with
    | hd::tl when hd > a -> find hd a b tl
    | _::tl -> find a b c tl
    | [] -> a + b + c
  in
  find 0 0 0 lst
;;

let run () =
  let elves = read_elves "inputs/d01.in" in
  Printf.printf "%d\n" (list_max elves);
  Printf.printf "%d\n" (top_three elves);
;;
