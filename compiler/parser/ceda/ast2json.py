#!/usr/bin/python3


import os;
from os import abort;


STRING_OF_VAR_TYPE_DICT = {
    "Normal"   : "",
    "Minus"    : "-",
    "Plus"     : "+",
    "Question" : "?",
    "Assign"   : "=",
    "TrimR"    : "%",
    "TrimRMax" : "%%",
    "TrimL"    : "#",
    "TrimLMax" : "##",
    "Length"   : "#"
};


# dash.ml
# let rec intercalate p ss =
#   match ss with
#   | [] -> ""
#   | [s] -> s
#   | s::ss -> s ^ p ^ intercalate p ss  
def intercalate (p, ss):
    str = "";

    i = 0;
    for s in ss:
        if (i > 0):
            str = str + p;

        str = str + s;

        i = i + 1;

    return (str);


# let braces s = "{ " ^ s ^ " ; }"
def braces (s):
    return "{ " + s + " ; }";


# let parens s = "( " ^ s ^ " )"
def parens (s):
    return "( " + s + " )";


# let string_of_var_type = function
#  | Normal -> ""
#  | Minus -> "-"
#  | Plus -> "+"
#  | Question -> "?"
#  | Assign -> "="
#  | TrimR -> "%"
#  | TrimRMax -> "%%"
#  | TrimL -> "#"
#  | TrimLMax -> "##" 
#  | Length -> "#" 
def string_of_var_type (var_type):
    if (var_type in STRING_OF_VAR_TYPE_DICT):
        return (STRING_OF_VAR_TYPE_DICT [var_type]);

    exit (1);


# let separated f l = intercalate " " (List.map f l)
def separated (f, l):
    return " ".join (map (f, l));


# let show_unless expected actual =
#   if expected = actual
#   then ""
#   else string_of_int actual
def show_unless (expected, actual):
    if (expected == actual):
        return "";
    else:
        return (str (actual));


# let background s = "{ " ^ s ^ " & }"
def background (s):
    return ("{ " + s + " & }");






# let rec to_string = function
#   | Command (_,assigns,cmds,redirs) ->
#      separated string_of_assign assigns ^
#      (if List.length assigns = 0 || List.length cmds = 0 then "" else " ") ^
#      separated string_of_arg cmds ^ string_of_redirs redirs
#   | Pipe (bg,ps) ->
#      let p = intercalate " | " (List.map to_string ps) in
#      if bg then background p else p
#   | Redir (_,a,redirs) ->
#      to_string a ^ string_of_redirs redirs
#   | Background (_,a,redirs) ->
#      (* we translate 
#            cmds... &
#         to
#            { cmds & }
#         this avoids issues with parsing; in particular,
#           cmd1 & ; cmd2 & ; cmd3
#         doesn't parse; it must be:
#           cmd1 & cmd2 & cmd3
#         it's a little too annoying to track "was the last thing
#         backgrounded?" so the braces resolve the issue. testing
#         indicates that they're semantically equivalent.
#       *)
#      background (to_string a ^ string_of_redirs redirs)
#   | Subshell (_,a,redirs) ->
#      parens (to_string a ^ string_of_redirs redirs)
#   | And (a1,a2) -> to_string  a1 ^ " && " ^ to_string a2
#   | Or (a1,a2) -> to_string a1 ^ " || " ^ to_string a2
#   | Not a -> "! " ^ braces (to_string a)
#   | Semi (a1,a2) -> to_string a1 ^ " ; " ^ to_string a2
#   | If (c,t,e) -> string_of_if c t e
#   | While (Not t,b) ->
#      "until " ^ to_string t ^ "; do " ^ to_string b ^ "; done "
#   | While (t,b) ->
#      "while " ^ to_string t ^ "; do " ^ to_string b ^ "; done "
#   | For (_,a,body,var) ->
#      "for " ^ var ^ " in " ^ string_of_arg a ^ "; do " ^
#      to_string body ^ "; done"
#   | Case (_,a,cs) ->
#      "case " ^ string_of_arg a ^ " in " ^
#      separated string_of_case cs ^ " esac"
#   | Defun (_,name,body) -> name ^ "() {\n" ^ to_string body ^ "\n}"
def to_string (ast):
    # print (ast);

    if (len (ast) == 0):
        pass;
    else:
        assert (len (ast) == 2);

        type = ast [0];
        params = ast [1]

        if (type == "Command"):
            (_, assigns, cmds, redirs) = params;
            str = separated (string_of_assign, assigns);
            if ((len (assigns) == 0) or (len (cmds) == 0)):
                pass;
            else:
                str = str + " ";
            str = str + separated (string_of_arg, cmds) + string_of_redirs (redirs);

            return (str);
        elif (type == "Pipe"):
            (bg, ps) = params;
            p = intercalate (" | ", (map (to_string, ps)));

            if (bg):
                return (background (p));
            else:
                return (p);
        elif (type == "Redir"):
            (_, a, redirs) = params;

            return to_string (a) + string_of_redirs (redirs);
        elif (type == "Background"):
            (_, a, redirs) = params;

            return background (to_string (a) + string_of_redirs (redirs));
        elif (type == "Subshell"):
            (_, a, redirs) = params;

            return parens (to_string (a) + string_of_redirs (redirs));
        elif (type == "And"):
            (a1, a2) = params;

            return to_string (a1) + " && " + to_string (a2);
        elif (type == "Or"):
            (a1, a2) = params;

            return to_string (a1) + " || " + to_string (a2);
        elif (type == "Not"):
            (a) = params;

            return "! " + to_string (a);
        elif (type == "Semi"):
            (a1, a2) = params;

            return to_string (a1) + " ; " + to_string (a2);
        elif (type == "If"):
            (c, t, e) = params;
            return string_of_if (c, t, e);
        elif (type == "While"):
            (first, b) = params;

            if (first [0] == "Not"):
                abort;
            else:
                t = first;

                return "while " + to_string (t) + "; do " + to_string (b) + "; done ";
        elif (type == "For"):
            abort ();
        elif (type == "Case"):
            abort ();
        elif (type == "Defun"):
            (_, name, body) = params;

            return name + "() {\n" + to_string (body) + "\n}";
        else:
            print ("Invalid type: %s" % type);
            abort ();







# and string_of_if c t e =
#   "if " ^ to_string c ^
#   "; then " ^ to_string t ^
#   (match e with
#    | Command (-1,[],[],[]) -> "; fi" (* one-armed if *)
#    | If (c,t,e) -> "; el" ^ string_of_if c t e
#    | _ -> "; else " ^ to_string e ^ "; fi")
def string_of_if (c, t, e):
    str = "if " + to_string (c) + \
          "; then " + to_string (t);

    # TODO: uncommon cases
    str = str + "; else " + to_string (e) + "; fi";

    return (str);



# and string_of_arg_char = function
#   | E '\'' -> "\\'"
#   | E '\"' -> "\\\""
#   | E '(' -> "\\("
#   | E ')' -> "\\)"
#   | E '{' -> "\\{"
#   | E '}' -> "\\}"
#   | E '$' -> "\\$"
#   | E '!' -> "\\!"
#   | E '&' -> "\\&"
#   | E '|' -> "\\|" 
#   | E ';' -> "\\;" 
#   | C c -> String.make 1 c
#   | E c -> Char.escaped c
#   | T None -> "~"
#   | T (Some u) -> "~" ^ u
#   | A a -> "$((" ^ string_of_arg a ^ "))"
#   | V (Length,_,name,_) -> "${#" ^ name ^ "}"
#   | V (vt,nul,name,a) ->
#      "${" ^ name ^ (if nul then ":" else "") ^ string_of_var_type vt ^ string_of_arg a ^ "}"
#   | Q a -> "\"" ^ string_of_arg a ^ "\""
#   | B t -> "$(" ^ to_string t ^ ")"
def string_of_arg_char (c):
    assert (len (c) == 2);

    (type, param) = c;

    if (type == "E"):
        char = chr (param);

        if (char == "'"):
            return "\\'";
        elif (char == "\""):
            return "\\\"";
        elif (char == "("):
            return "\\(";
        elif (char == ")"):
            return "\\)";
        elif (char == "{"):
            return "\\{";
        elif (char == "}"):
            return "\\}";
        elif (char == "$"):
            return "\\$";
        elif (char == "!"):
            return "\\!";
        elif (char == "&"):
            return "\\&";
        elif (char == "|"):
            return "\\|";
        elif (char == ";"):
            return "\\;";
        elif (char == "\\"):
            return "\\\\";
        elif (char == "\t"):
            return "\\t";
        else:
            if ((param < 32) or (param > 126)):
                return ("\\" + str (param));
            else:
                return (char);

        return "TODO11";
    elif (type == "C"):
        return chr (param);
    elif (type == "T"):
        return "TODO12";
    elif (type == "A"):
        return "TODO13";
    elif (type == "V"):
        assert (len (param) == 4);
        if (param [0] == "Length"):
            (_, _, name, _) = param;
            return "${#" + name + "}";
        else:
            (vt, nul, name, a) = param;

            str = "${" + name;
            if (nul):
                str = str + ":";

            str = str + string_of_var_type (vt) + string_of_arg (a) + "}";

            return str;
    elif (type == "Q"):
        return "\"" + string_of_arg (param) + "\"";
    elif (type == "B"):
        return "$(" + to_string (param) + ")";
    else:
        abort ();


# and string_of_arg = function
#   | [] -> ""
#   | c :: a -> string_of_arg_char c ^ string_of_arg a
def string_of_arg (args):
    if (len (args) == 0):
        return "";
    else:
        c = args [0];
        a = args [1:];

        return string_of_arg_char (c) + string_of_arg (a);


# and string_of_assign (v,a) = v ^ "=" ^ string_of_arg a
def string_of_assign (both):
    (v, a) = both;
    return v + "=" + string_of_arg (a);


#                                                    
# and string_of_case c =
#   let pats = List.map string_of_arg c.cpattern in
#   intercalate "|" pats ^ ") " ^ to_string c.cbody ^ ";;"
# 
# and string_of_redir = function
#   | File (To,fd,a)      -> show_unless 1 fd ^ ">" ^ string_of_arg a
#   | File (Clobber,fd,a) -> show_unless 1 fd ^ ">|" ^ string_of_arg a
#   | File (From,fd,a)    -> show_unless 0 fd ^ "<" ^ string_of_arg a
#   | File (FromTo,fd,a)  -> show_unless 0 fd ^ "<>" ^ string_of_arg a
#   | File (Append,fd,a)  -> show_unless 1 fd ^ ">>" ^ string_of_arg a

#   | Dup (ToFD,fd,tgt)   -> show_unless 1 fd ^ ">&" ^ string_of_arg tgt
#   | Dup (FromFD,fd,tgt) -> show_unless 0 fd ^ "<&" ^ string_of_arg tgt
#   | Heredoc (t,fd,a) ->
#      let heredoc = string_of_arg a in
#      let marker = fresh_marker (lines heredoc) "EOF" in
#      show_unless 0 fd ^ "<<" ^
#      (if t = XHere then marker else "'" ^ marker ^ "'") ^ "\n" ^ heredoc ^ marker ^ "\n"
def string_of_redir (redir):
    assert (len (redir) == 2);

    (type, param) = redir;
    if (type == "File"):
        assert (len (param) == 3);

        (subtype, fd, a) = param;
        if (subtype == "To"):
            return (show_unless (1, fd) + ">" + string_of_arg (a));
        elif (subtype == "Clobber"):
            return (show_unless (1, fd) + ">|" + string_of_arg (a));
        elif (subtype == "From"):
            return (show_unless (0, fd) + "<" + string_of_arg (a));
        elif (subtype == "FromTo"):
            return (show_unless (0, fd) + "<>" + string_of_arg (a));
        elif (subtype == "Append"):
            return (show_unless (1, fd) + ">>" + string_of_arg (a));
        else:
            abort ();
    else:
        abort ();

    return "TODO";


# and string_of_redirs rs =
#   let ss = List.map string_of_redir rs in
#   (if List.length ss > 0 then " " else "") ^ intercalate " " ss
def string_of_redirs (rs):
    str = "";

    for redir in rs:
        str = str + " " + string_of_redir (redir);

    return (str);

