module ctr(input clk, rst, ctrl, output reg[3:0] O);
    reg [1:0] state;
    always @(posedge clk) begin
        O <= 0;
        if (rst) begin
            state <= 0;
        end
        else 
        case (state)
            0: begin
                if (ctrl) begin
                    O <= 2 * 3;
                    state <= 1;
                end
                else begin
                    O <= 1 + 2;
                    state <= 2;
                end
            end
            1: begin
                O <= 4 / 2;
                if (ctrl) begin
                    state <= 2;
                    O <= 3 ^ 2;
                end
            end
            2: begin
                O <= 4;
                if (ctrl) begin
                    state <= 3;
                    O <= 5 - 4;
                end
            end
            3: begin
                if (!ctrl)
                    state <= 2'b00;
            end
        endcase
    end
endmodule