#include <iostream>
#include <string>
#include <fstream>
#include <filesystem>

namespace fs = std::filesystem;

class Good
{
public:
    Good() = default;
    Good(std::string naming, unsigned quantity, double price)
        : naming_(std::move(naming)), quantity_(quantity), price_(price) {}

    friend std::ostream &operator<<(std::ostream &os, const Good &good)
    {
        os << "Naming, Quantity, Price, Total" << std::endl;
        os << good.naming_ << ", " << good.quantity_ << ", " << good.price_ << ", " << good.getTotalCost() << std::endl;

        return os;
    }

    friend std::istream &operator>>(std::istream &is, Good &good)
    {
        std::cout << "Enter naming: ";
        is >> good.naming_;

        std::cout << "Enter quantity: ";
        is >> good.quantity_;

        std::cout << "Enter price: ";
        is >> good.price_;

        return is;
    }

    std::string naming() const
    {
        return naming_;
    }

private:
    std::string naming_;
    unsigned quantity_;
    double price_;

    double getTotalCost() const
    {
        return quantity_ * price_;
    }
};

void writeToFile(const Good &good)
{
    const std::string filename = good.naming() + ".csv";

    std::cout << "Saving following content to " + filename + ":\n";
    std::cout << good << std::endl;

    std::fstream file(filename, std::ios::out);
    file << good;
    file.close();
}

enum Option
{
    Quit,
    Add,
    Check
};

Option getOption()
{
    std::cout << "Choose an option: " << std::endl;
    std::cout << "1: Add good." << std::endl;
    std::cout << "2: Check good." << std::endl;
    std::cout << "0: Exit." << std::endl;

    int option;
    std::cin >> option;
    getchar(); // for \n

    return (Option)option;
}

void handleAdd()
{
    Good good;
    std::cin >> good;
    writeToFile(good);
}

void handleCheck()
{
    std::string naming;
    std::cout << "Enter good naming to check: ";
    std::cin >> naming;

    const std::string filename = naming + ".csv";
    if (fs::exists(fs::path{filename}))
    {
        std::fstream file(filename, std::ios::in);
        if (!file.is_open())
        {
            std::cerr << "Error loading file contents." << std::endl;
            return;
        }
        std::cout << file.rdbuf();

        file.close();
    }
    else
    {
        std::cout << "Seems like this good does not exist." << std::endl;
    }
}

void handleDefault()
{
    std::cout << "Invalid option!" << std::endl;
}

int main()
{
    std::string buffer;
    bool running = true;

    while (running)
    {
        Option option = getOption();

        switch (option)
        {
        case Option::Quit:
            running = false;
            break;
        case Option::Add:
            handleAdd();
            break;
        case Option::Check:
            handleCheck();
            break;

        default:
            handleDefault();
        }
    }
    return 0;
}
