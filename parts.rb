#!/usr/bin/env ruby

file = File.read "names.csv"
lines = file.split "\n"
n = 0
lines.each do |line|
  n += 1
  if( n % 100 == 1 )  
    puts line.chomp
  end
end

